#!/usr/bin/env python
# coding=utf-8
from pytest import fixture, raises

from json_config.main import AutoSyncMixin, AutoDict

CONFIG = 'config.json'


@fixture
def auto_save(tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""

    class AutoSave(AutoSyncMixin, AutoDict):
        pass

    _auto_save = AutoSave()
    _auto_save.config_file = tmpdir.join(CONFIG).strpath

    return _auto_save


def test_saves_on_setting_leaf(auto_save, tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""
    auto_save['this']['is']['a']['test'] = 'success'

    with tmpdir.join(CONFIG).open() as f:
        result = f.read()

    assert result == "{'this': {'is': {'a': {'test': 'success'}}}}"


def test_saves_on_setting_leaf_to_empty_dict(auto_save, tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""
    auto_save['this']['is']['a']['test'] = {}

    with tmpdir.join(CONFIG).open() as f:
        result = f.read()

    assert result == "{'this': {'is': {'a': {'test': {}}}}}"


def test_does_not_save_by_declaring_a_ton_of_unused_keys(auto_save, tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""

    # noinspection PyStatementEffect
    auto_save['this']['is']['a']['test']

    with raises(OSError):
        f = open(tmpdir.join(CONFIG).strpath)
        f.close()


def test_only_saves_once_per_setting_value(auto_save, mocker):
    mocker.spy(auto_save, 'save')
    assert auto_save.save.call_count == 0

    auto_save['this']['is']['a']['test'] = 'success'
    assert auto_save.save.call_count == 1

    auto_save['completely']['different']['tree']['and']['different']['depth'] = 'hello'
    assert auto_save.save.call_count == 2
