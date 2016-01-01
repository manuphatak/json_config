#!/usr/bin/env python
# coding=utf-8
import json
from collections import defaultdict
from contextlib import contextmanager

from ._compat import FileNotFoundError
from .contracts import AbstractTraceRoot, AbstractSaveFile, AbstractSerializer


class TraceRootMixin(AbstractTraceRoot):
    _lock_ = None

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

    @property
    def _parent(self):
        if self._is_root:
            return False

        return self._parent_[0]

    @_parent.setter
    def _parent(self, value):
        if isinstance(value, (list, tuple)):
            self._parent_ = value
        else:
            self._parent_ = [value]

    @property
    def _lock(self):
        return self._root._lock_

    @_lock.setter
    def _lock(self, value):
        self._root._lock_ = value

    @property
    def _islocked(self):
        return not self._lock is None

    @contextmanager
    def lock(self):
        is_lock_owner = False
        try:
            if not self._islocked:
                self._lock = self
                is_lock_owner = True
            yield is_lock_owner
        finally:
            if is_lock_owner:
                self._lock = None


class AutoDict(TraceRootMixin, defaultdict):
    def __init__(self, obj=None, _root=None, _parent=None, _key=None):
        super(AutoDict, self).__init__()

        if _root is None:
            self._root = self
        else:
            self._root = _root

        self._parent = _parent
        self._key = _key

        if obj is not None:
            with self.lock():
                self.update(obj)

    def __missing__(self, key):
        _AutoDict = self.__class__
        self[key] = value = _AutoDict(_root=self._root, _parent=self, _key=key)
        return value

    def __setitem__(self, key, value):
        _AutoDict = self.__class__

        # convert dicts to AutoDicts
        is_dict = not isinstance(value, _AutoDict) and isinstance(value, dict)
        if is_dict:
            value = _AutoDict(obj=value, _root=self._root, _parent=self, _key=key)

        super(AutoDict, self).__setitem__(key, value)

    def __delitem__(self, key):
        super(AutoDict, self).__delitem__(key)

        if self._is_root:
            return self._root.save()

        if self._parent[self._key] == {}:
            del self._parent[self._key]
        else:
            self._root.save()

    def update(self, E=None, **F):
        """
        D.update(E, **F) -> None.  Update D from E and F: for k in E: D[k]
                = E[k]
        (if E has keys else: for (k, v) in E: D[k] = v) then: for k in
                F: D[k] = F[k]
        """
        _AutoDict = self.__class__

        def update_or_set(key, value):
            if isinstance(value, dict):
                self[key] = _AutoDict(obj=value, _root=self._root, _parent=self, _key=key)
            else:
                self[key] = value

        with self.lock() as lock_owner:
            # update E
            if hasattr(E, 'keys') and callable(E.keys):
                for key in E:
                    update_or_set(key, E[key])
            else:
                for key, value in E:
                    update_or_set(key, value)

            # update F
            for key in F:
                update_or_set(key, F[key])

            # save if original caller.
            if lock_owner:
                self._root.save()

    def save(self):
        pass

    # noinspection PyMethodOverriding
    def __repr__(self):
        if self._is_root:
            cls_name = self.__class__.__name__
            return '%s(%s)' % (cls_name, dict(self))

        return repr(dict(self))

    def __str__(self):
        return repr(self)

    def __unicode__(self):
        return repr(self)


class AutoSyncMixin(AbstractSaveFile, AbstractTraceRoot, AbstractSerializer):
    def __init__(self, **kwargs):
        config_file = kwargs.pop('config_file', None)
        """:type config_file: str|None"""

        if config_file is not None:
            self.config_file = config_file

            try:
                with open(config_file) as f:
                    string = f.read()
                obj = self.deserialize(string)
                kwargs.setdefault('obj', obj)
            except FileNotFoundError:
                pass

        # noinspection PyUnresolvedReferences
        super(AutoSyncMixin, self).__init__(**kwargs)

    def __setitem__(self, key, value):
        # noinspection PyUnresolvedReferences
        super(AutoSyncMixin, self).__setitem__(key, value)

        is_cls = isinstance(self[key], self.__class__)
        if not is_cls and not self._islocked:
            self._root.save()

    def save(self):
        if not self._is_root:
            raise RuntimeError('Trying to save from wrong node.')

        with open(self.config_file, 'w') as f:
            f.write(self.serialize())


class PrettyJSONMixin(AbstractSerializer):
    serializer_indent = 2
    serializer_sort_keys = True
    serializer_ext = 'json'

    def deserialize(self, string):
        return json.loads(string)

    def serialize(self, **options):
        options.setdefault('indent', self.serializer_indent)
        options.setdefault('sort_keys', self.serializer_sort_keys)
        options.setdefault('separators', (',', ': '))

        return json.dumps(dict(self), **options)


class AutoConfigBase(AutoSyncMixin, AutoDict):
    def __init__(self, config_file=None, **kwargs):
        # normalize kwargs
        kwargs.setdefault('config_file', config_file)
        super(AutoConfigBase, self).__init__(**kwargs)


def connect(config_file, file_type=None, **kwargs):
    if file_type is None:
        file_type = str(config_file).rsplit('.', 1)[-1]

    AbstractSerializers = AbstractSerializer.__subclasses__()

    try:
        # noinspection PyPep8Naming
        Serializer = [  # :off
            cls
            for cls in AbstractSerializers
            if cls.serializer_ext == file_type
        ][-1] # :on
    except IndexError:
        Serializer = PrettyJSONMixin

    class Connect(Serializer, AutoConfigBase):
        pass

    return Connect(config_file, **kwargs)
