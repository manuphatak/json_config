#!/usr/bin/env python
# coding=utf-8
"""
A convenience utility for working with JSON config files.
"""

import json
import threading
from functools import wraps, partial
from collections import defaultdict

pprint = True


class ConfigObject(defaultdict):
    _container = None
    """Reference to the parent node"""

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
            self_.block()
            with open(config_file) as f:
                self_.update(json.load(f, object_hook=json_hook))
        except IOError:
            with open(config_file, 'w') as f:
                f.close()  # open + close required for pypy

        return self_

    @classmethod
    def parent_node(cls, config_file):
        """
        Create a parent node, with special parent properties.

        :param string config_file: Path to JSON file.
        :return: self.
        :rtype : ConfigObject
        """
        self = cls(config_file=config_file)
        self._container = self
        self.timer = None
        return self

    @classmethod
    def child_node(cls, parent, *obj):
        """
        Create a child node with a reference to the parent.

        :param parent: Reference to the parent node.
        :param obj: Values to be stored.
        :return: self
        :rtype : ConfigObject
        """
        self = cls(parent=parent)
        self.update(*obj)
        return self

    def save_config(*method_arguments):
        """
        Decorator.  Start the delayed worker to save the file after a series
        of calls.

        :param method_arguments: a hack for method decorators.
        :return: decorated method
        """
        function = method_arguments[-1]
        """A hack for method decorators"""

        @wraps(function)
        def _wrapper(self, *args, **kwargs):
            """Cancel save attempts  until series of requests is complete."""
            try:
                if self._container.timer:
                    self._container.timer.cancel()
                return function(self, *args, **kwargs)

            finally:
                save = self._container.write_file
                self._container.timer = threading.Timer(0.001, save)
                self._container.timer.name = self._container.config_file
                self._container.timer.start()

        return _wrapper

    def write_file(self):
        """
        Write the JSON config file to disk.
        """
        if not self.config_file:
            raise RuntimeError('Missing Config File')

        with open(self.config_file, 'w') as f:
            f.write(repr(self._container))

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

    def block(self):
        """
        Block until writing threads are completed.

        This is mostly for internal use and testing.  If you plan to connect
        to a file being managed to this tool, use this to make sure the file
        safe to read and write on.
        """
        save_config_threads = [thread for thread in threading.enumerate() if
                               thread.name == self._container.config_file]

        for save_config_thread in save_config_threads:
            save_config_thread.join()

# export
connect = ConfigObject.connect
