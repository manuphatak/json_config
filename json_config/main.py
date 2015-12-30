#!/usr/bin/env python
# coding=utf-8
from collections import defaultdict, namedtuple

AutoDictRepr = namedtuple('AutoDict', ['dict'])


class TrackRootMixin(object):
    _root_ = NotImplemented

    @property
    def _is_root(self):
        return self._root is self

    @property
    def _root(self):
        return self._root_[0]

    @_root.setter
    def _root(self, value):
        if isinstance(value, (list, tuple)):
            self._root_ = value
        else:
            self._root_ = [value]


class AutoDict(TrackRootMixin, defaultdict):
    def __init__(self, obj=None, root=None):
        super(AutoDict, self).__init__()
        if obj is not None:
            self.update(obj)

        if root is None:
            self._root = self
        else:
            self._root = root

    def __missing__(self, key):
        AutoDict = self.__class__
        self[key] = value = AutoDict(root=self._root)
        return value

    def __repr__(self):
        if self._is_root:
            return repr(AutoDictRepr(dict(self)))

        return repr(dict(self))


class FileSync(AutoDict):
    pass
