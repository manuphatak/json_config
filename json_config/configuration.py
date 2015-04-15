#!/usr/bin/env python
# coding=utf-8
"""
A convenience utility for working with JSON config files.
"""
from functools import wraps
import json
from collections import MutableMapping, defaultdict

config_file = None
config = None


def connect(config_file_):
    """
    Connect to a json config file.

    Returns a python dict-like object.  Automatically syncs with the file.
    Automatically handles  nested data.

    :param str config_file_: String path pointing to json file.
    :return: Dictionary like python object.
    """
    global config_file
    global config

    config_file = config_file_
    config = Configuration()

    try:
        config.update(json.load(open(config_file), object_hook=json_hook))
    except IOError:
        with open(config_file, 'w') as f:
            f.close()

    return config


def json_hook(obj):
    config_ = Configuration()
    config_.update(**obj)
    return config_


class Configuration(defaultdict, MutableMapping):
    """
    Internal class.  Handles nested dictionary recursion.
    """

    def save_config(*func_args):
        """
        Decorator.  Write the config file after execution.

        :param func_args: a hack for method decorators.
        :return: decorated method
        """
        func = func_args[-1]

        @wraps(func)
        def _wrapper(self, *args, **kwargs):

            try:
                return func(self, *args, **kwargs)

            finally:
                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=2, sort_keys=True, separators=(',', ': '))

        return _wrapper

    def __init__(self, **kwargs):
        super(Configuration, self).__init__(self.factory, **kwargs)

    @save_config
    def __setitem__(self, key, value):
        super(Configuration, self).__setitem__(key, value)

    def __getitem__(self, key):
        return super(Configuration, self).__getitem__(key)

    @save_config
    def __delitem__(self, key):
        super(Configuration, self).__delitem__(key)

    def __repr__(self):
        return json.dumps(self, indent=2, sort_keys=True, separators=(',', ': '))

    @staticmethod
    def factory():
        """
        Lazy load child instance of self.

        :return:
        """
        return Configuration()
