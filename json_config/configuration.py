#!/usr/bin/env python
# coding=utf-8
"""
A convenience utility for working with JSON config files.
"""
from functools import wraps, partial
from collections import defaultdict
import json

pprint = True


class ConfigObject(defaultdict):
    _container = None

    def __init__(self, parent=None, config_file=None):
        self.config_file = config_file
        super(ConfigObject, self).__init__(self.factory)
        self._container = parent

    @classmethod
    def connect(cls, config_file):
        """
        Connect to a json config file.

        Returns a python dict-like object.  Automatically syncs with the file.
        Automatically handles  nested data.

        :param str config_file: String path pointing to json file.
        :return: Dictionary like python object.
        """
        self_ = cls.parent_node(config_file=config_file)
        json_hook = partial(cls.child_node, self_)
        try:
            self_.update(json.load(open(config_file), object_hook=json_hook))
        except IOError:
            with open(config_file, 'w') as f:  # open + close required for pypy
                f.close()

        return self_

    @classmethod
    def parent_node(cls, config_file):
        self = cls(config_file=config_file)
        self._container = self
        return self

    @classmethod
    def child_node(cls, parent, *obj):
        self = cls(parent=parent)
        self.update(*obj)
        return self

    def save_config(*method_arguments):
        """
        Decorator.  Write the config file after execution if is parent node
        and is changed.

        :param method_arguments: a hack for method decorators.
        :return: decorated method
        """
        function = method_arguments[-1]

        @wraps(function)
        def _wrapper(self, *args, **kwargs):
            """Set state. Continue.  Check state for changes.  Save."""
            # before_hash = hash(self._container)
            try:
                return function(self, *args, **kwargs)

            finally:
                # after_hash = hash(self._container)
                #
                # has_changed = not before_hash == after_hash

                # if has_changed and is_parent:
                self._container.write_file()

        return _wrapper

    def write_file(self):  # extracted for testing
        if not hash(self._container) == hash(self):
            raise Exception('Not the container')

        if not self.config_file:
            raise Exception('Missing Config File')

        with open(self.config_file, 'w') as f:
            f.write(repr(self))

    @save_config
    def __setitem__(self, key, value):
        super(ConfigObject, self).__setitem__(key, value)
        return self

    @save_config
    def __delitem__(self, key):
        super(ConfigObject, self).__delitem__(key)
        return self

    def factory(self):
        """
        Lazy load child instance of self.

        :return:
        """
        return ConfigObject.child_node(parent=self._container)

    @staticmethod
    def pformat(obj):
        """
        Pretty Print JSON output.

        :param obj:
        :return:
        """
        return json.dumps(obj, indent=2, sort_keys=True, separators=(',', ': '))

    def __repr__(self):
        return json.dumps(self) if not pprint else self.pformat(self)

    def __hash__(self):
        return hash(str(self))

# export
connect = ConfigObject.connect
