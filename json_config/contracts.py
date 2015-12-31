#!/usr/bin/env python
# coding=utf-8

from abc import ABCMeta, abstractproperty, abstractmethod
from future.utils import with_metaclass


class AbstractTraceRoot(with_metaclass(ABCMeta)):  # pragma: no cover
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


class AbstractSerializer(with_metaclass(ABCMeta)):  # pragma: no cover
    serializer_ext = NotImplemented

    @abstractmethod
    def deserialize(self, string):
        pass

    @abstractmethod
    def serialize(self, **options):
        pass


class AbstractSaveFile(with_metaclass(ABCMeta)):  # pragma: no cover
    config_file = NotImplemented

    @abstractmethod
    def save(self):
        pass
