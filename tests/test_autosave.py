#!/usr/bin/env python
# coding=utf-8
from _pytest.python import raises
from pytest import fixture

from json_config.main import AutoSaveMixin, AutoDict

CONFIG = 'config.json'


@fixture
def auto(tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""

    class AutoSave(AutoSaveMixin, AutoDict):
        pass

    _auto = AutoSave()
    _auto.config_file = str(tmpdir.join(CONFIG))

    return _auto


def test_saves_on_setting_leaf(auto, tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""
    auto['this']['is']['a']['test'] = 'success'

    with tmpdir.join(CONFIG).open() as f:
        result = f.read()

    assert result == "{'this': {'is': {'a': {'test': 'success'}}}}"


def test_saves_on_setting_leaf_to_empty_dict(auto, tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""
    auto['this']['is']['a']['test'] = {}

    with tmpdir.join(CONFIG).open() as f:
        result = f.read()

    assert result == "{'this': {'is': {'a': {'test': {}}}}}"


def test_does_not_save_by_declaring_a_ton_of_unused_keys(auto, tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""

    # noinspection PyStatementEffect
    auto['this']['is']['a']['test']

    with raises(OSError):
        f = open(str(tmpdir.join(CONFIG)))
        f.close()


def test_only_saves_once_per_setting_value(auto, mocker):
    mocker.spy(auto, 'save')
    assert auto.save.call_count == 0

    auto['this']['is']['a']['test'] = 'success'
    assert auto.save.call_count == 1

    auto['completely']['different']['tree']['and']['different']['depth'] = 'hello'
    assert auto.save.call_count == 2
