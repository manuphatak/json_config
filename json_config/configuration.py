#!/usr/bin/env python
# coding=utf-8
"""
A convenience utility for working with JSON config files.
"""
from functools import wraps, partial
import json
from collections import defaultdict

pprint = True


class ConfigObject(defaultdict):
    __container = {}

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
            before_hash = hash(self.__container)
            try:
                return function(self, *args, **kwargs)

            finally:
                after_hash = hash(self.__container)

                has_changed = not before_hash == after_hash
                is_parent = after_hash == hash(self) and self.__config_file

                if has_changed and is_parent:
                    self._write_file(self.__config_file, repr(self))

        return _wrapper

    def factory(self):
        """
        Lazy load child instance of self.

        :return:
        """
        return ConfigObject.child_node(parent=self.__container)

    @staticmethod
    def pformat(obj):
        """
        Pretty Print JSON output.

        :param obj:
        :return:
        """
        return json.dumps(obj, indent=2, sort_keys=True, separators=(',', ': '))

    @staticmethod
    def _write_file(config_file, content):  # extracted for testing
        with open(config_file, 'w') as f:
            f.write(content)

    @classmethod
    def child_node(cls, *obj, **kwargs):
        self = cls(parent=kwargs['parent'])
        self.update(*obj)
        return self

    @classmethod
    def parent_node(cls, **kwargs):
        self = cls(config_file=kwargs['config_file'], parent=False)
        return self

    @classmethod
    def connect(cls, config_file):
        """
        Connect to a json config file.

        Returns a python dict-like object.  Automatically syncs with the file.
        Automatically handles  nested data.

        :param str config_file: String path pointing to json file.
        :return: Dictionary like python object.
        """
        self = cls.parent_node(config_file=config_file)
        json_hook = partial(cls.child_node, parent=self)
        try:
            self.update(json.load(open(config_file), object_hook=json_hook))
        except IOError:
            with open(config_file, 'w') as f:  # open + close required for pypy
                f.close()

        return self

    def __init__(self, parent, config_file=None, **kwargs):
        self.__container = (parent or self)
        self.__config_file = config_file
        super(ConfigObject, self).__init__(self.factory, **kwargs)

    @save_config
    def __setitem__(self, key, value):
        super(ConfigObject, self).__setitem__(key, value)
        return self

    @save_config
    def __delitem__(self, key):
        super(ConfigObject, self).__delitem__(key)
        return self

    @save_config
    def __getitem__(self, key):
        return super(ConfigObject, self).__getitem__(key)

    def __repr__(self):
        return json.dumps(self) if not pprint else self.pformat(self)

    def __hash__(self):
        return hash(str(self))

# export
connect = ConfigObject.connect
