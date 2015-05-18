#!/usr/bin/env python
# coding=utf-8
"""
A convenience utility for working with JSON config files.
"""
from functools import wraps, partial
from collections import defaultdict
import json
from threading import Timer
from io import FileIO
import threading

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
            self_.block()
            with FileIO(config_file) as f:
                self_.update(json.load(f, object_hook=json_hook))
        except IOError:
            with FileIO(config_file, 'w') as f:
                f.close()  # open + close required for pypy

        return self_

    @classmethod
    def parent_node(cls, config_file):
        self = cls(config_file=config_file)
        self._container = self
        self.timer = None
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
            """Save after changes."""
            try:
                if self._container.timer:
                    self._container.timer.cancel()
                    # print('cancelling thread')
                return function(self, *args, **kwargs)

            finally:
                save = self._container.write_file
                self._container.timer = Timer(0.001, save)
                self._container.timer.name = self._container.config_file
                # print('starting thread')
                self._container.timer.start()

                # self._container.write_file()

        return _wrapper

    def write_file(self):  # extracted for testing
        # print('executing thread')
        if not self.config_file:
            raise RuntimeError('Missing Config File')

        with FileIO(self.config_file, mode='w') as f:
            f.write(repr(self._container))
            f.close()

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
        save_config_threads = [thread for thread in threading.enumerate() if
                               thread.name == self._container.config_file]

        for save_config_thread in save_config_threads:
            save_config_thread.join()

# export
connect = ConfigObject.connect
