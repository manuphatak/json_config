#!/usr/bin/env python
# coding=utf-8
import json
import shutil

from pytest import fixture, raises

from json_config.main import AutoConfigBase
from tests.utils import dir_tests

CONFIG = 'config.json'

SAMPLE_CONFIG = 'sample_assets/sample_config.json'
SAMPLE_CONFIG_LARGE = 'sample_assets/sample_config.json'


class AutoSave(AutoConfigBase):
    def serialize(self):
        return str(dict(self))


class AutoLoad(AutoConfigBase):
    def deserialize(self, string):
        return json.loads(string)


@fixture
def auto_save(tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""

    return AutoSave(config_file=tmpdir.join(CONFIG).strpath)


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

    with raises(IOError):
        f = open(tmpdir.join(CONFIG).strpath)
        f.close()


def test_only_saves_once_per_setting_value(auto_save, mocker):
    """:type mocker: pytest_mock.MockFixture"""

    mocker.spy(auto_save, u'save')
    assert auto_save.save.call_count == 0

    auto_save['this']['is']['a']['test'] = 'success'
    assert auto_save.save.call_count == 1

    auto_save['completely']['different']['tree']['and']['different']['depth'] = 'hello'
    assert auto_save.save.call_count == 2


def test_automatically_loads_config_file(tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""
    # setup
    shutil.copytree(dir_tests('sample_assets'), tmpdir.join('sample_assets').strpath)
    auto_load = AutoLoad(config_file=tmpdir.join(SAMPLE_CONFIG).strpath)

    expected = {
        'cat_2': 'cat_2 value', 'cat_3': {
            'sub_1': {
                'sub_sub_1': 'sub_sub_1 value',
                'sub_sub_2': {'sub_sub_sub_2': 'sub_sub_sub_2', 'sub_sub_sub_1': 'sub_sub_sub_1'}
            }
        }, 'test': 'success', 'cat_1': {
            'sub_1': {'sub_sub_1': {'sub_sub_sub_2': 'sub_sub_sub_2 value', 'sub_sub_sub_1': 'sub_sub_sub_1 value'}}
        }, 'cat_4': {
            '1': {'cat': {'nested_list': 'nested_list value'}}, '0': {'cat': 'cat value 0'}, '2': {'cat': 'cat value 2'}
        }
    }

    assert auto_load == expected


def test_handles_empty_config_file(tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""

    class BasicConfig(AutoLoad, AutoSave):
        pass

    empty = tmpdir.join('empty.json')
    auto_load = BasicConfig(config_file=empty.strpath)

    assert auto_load == {}

    auto_load['this']['is']['a']['test'] = 'success'

    with empty.open() as f:
        results = f.read()
    assert results == "{'this': {'is': {'a': {'test': 'success'}}}}"


def test_deleting_items_only_saves_once():
    # TODO
    pass


def test_deleting_nested_item_only_saves_once():
    # TODO
    pass
