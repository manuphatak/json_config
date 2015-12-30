#!/usr/bin/env python
# coding=utf-8
from abc import ABCMeta, abstractproperty, abstractmethod
from collections import defaultdict

from future.utils import with_metaclass


class TraceRoot(with_metaclass(ABCMeta)):
    @property
    @abstractproperty
    def _is_root(self):
        pass

    @property
    @abstractproperty
    def _root(self):
        pass

    @_root.setter
    @abstractproperty
    def _root(self, value):
        pass


class PrettyFormat(with_metaclass(ABCMeta)):
    @abstractmethod
    def pformat(self):
        pass


class TraceRootMixin(TraceRoot):
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


class AutoDict(TraceRootMixin, defaultdict):
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
            cls_name = self.__class__.__name__
            return '%s(%s)' % (cls_name, dict(self))

        return repr(dict(self))


class AutoSaveMixin(TraceRoot, PrettyFormat):
    config_file = NotImplemented

    def __setitem__(self, key, value):
        # noinspection PyUnresolvedReferences
        super(AutoSaveMixin, self).__setitem__(key, value)

        if not isinstance(value, self.__class__):
            self._root.save()

    def save(self):
        if not self._is_root:
            raise RuntimeError('Trying to save from wrong node.')
        with open(self.config_file, 'w') as f:
            f.write(self.pformat())

    def pformat(self):
        return str(dict(self))
