#!/usr/bin/env python
# coding=utf-8
"""
A convenience utility for working with JSON config files.
"""
from functools import wraps, partial
import json
from collections import defaultdict

pprint = True


def connect(config_file):
    """
    Connect to a json config file.

    Returns a python dict-like object.  Automatically syncs with the file.
    Automatically handles  nested data.

    :param str config_file: String path pointing to json file.
    :return: Dictionary like python object.
    """
    config = ConfigObject(config_file=config_file)
    json_hook = partial(ConfigObject.new, config_file=config_file, parent=[config])
    try:
        config.update(json.load(open(config_file), object_hook=json_hook))
    except IOError:
        with open(config_file, 'w') as f:  # open + close required for pypy
            f.close()

    return config


class ConfigObject(defaultdict):
    __parent = None

    def save_config(*func_args):
        """
        Decorator.  Write the config file after execution.

        :param func_args: a hack for method decorators.
        :return: decorated method
        """
        func = func_args[-1]

        @wraps(func)
        def _wrapper(self, *args, **kwargs):
            base = self.__parent[0] if self.__parent else self
            base_hash = hash(self.pformat(base))
            try:
                return func(self, *args, **kwargs)

            finally:
                if not base_hash == hash(self.pformat(base)):

                    with open(self.__config_file, 'w') as f:
                        f.write(repr(base))

        return _wrapper

    def factory(self):
        """
        Lazy load child instance of self.

        :return:
        """
        return ConfigObject(config_file=self.__config_file)

    @staticmethod
    def pformat(obj):
        return json.dumps(obj, indent=2, sort_keys=True, separators=(',', ': '))

    @classmethod
    def new(cls, *obj, **kwargs):
        self = cls(config_file=kwargs['config_file'], parent=kwargs['parent'])
        self.update(*obj)
        return self

    def __init__(self, config_file=None, parent=0, **kwargs):
        self.__parent = parent
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
