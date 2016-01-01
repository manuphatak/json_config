#!/usr/bin/env python
# coding=utf-8
import json
import shutil

from pytest import fixture, raises

from json_config.main import AutoConfigBase
from tests.utils import dir_tests

CONFIG = 'config.json'

SAMPLE_CONFIG_SMALL = 'sample_assets/sample_config_small.json'
SAMPLE_CONFIG_LARGE = 'sample_assets/sample_config_large.json'


class AutoJSON(AutoConfigBase):
    def serialize(self):
        return json.dumps(dict(self), sort_keys=True)

    def deserialize(self, string):
        return json.loads(string)


@fixture
def auto_save(tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""

    return AutoJSON(config_file=tmpdir.join(CONFIG).strpath)


def test_saves_on_setting_leaf(auto_save, tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""
    auto_save['this']['is']['a']['test'] = 'success'

    with tmpdir.join(CONFIG).open() as f:
        result = f.read()

    assert result == '{"this": {"is": {"a": {"test": "success"}}}}'


def test_does_not_save_on_setting_leaf_to_empty_dict(auto_save, tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""
    auto_save['this']['is']['a']['test'] = {}

    assert not tmpdir.join(CONFIG).exists()


def test_does_not_save_by_declaring_a_ton_of_unused_keys(auto_save, tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""

    # noinspection PyStatementEffect
    auto_save['this']['is']['a']['test']

    with raises(IOError):
        f = open(tmpdir.join(CONFIG).strpath)
        f.close()


# noinspection PyUnresolvedReferences
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
    auto_load = AutoJSON(config_file=tmpdir.join(SAMPLE_CONFIG_SMALL).strpath)

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

    empty = tmpdir.join('empty.json')
    auto_load = AutoJSON(config_file=empty.strpath)

    assert auto_load == {}

    auto_load['this']['is']['a']['test'] = 'success'

    with empty.open() as f:
        results = f.read()
    assert results == '{"this": {"is": {"a": {"test": "success"}}}}'


# noinspection PyUnresolvedReferences
def test_deleting_items_only_saves_once(auto_save, mocker):
    """:type mocker: pytest_mock.MockFixture"""
    mocker.spy(auto_save, u'save')

    auto_save['this']['is']['a']['test'] = 'success'

    auto_save.save.reset_mock()
    assert auto_save.save.call_count == 0

    del auto_save['this']['is']['a']['test']
    assert auto_save.save.call_count == 1


# noinspection PyUnresolvedReferences
def test_deleting_nested_item_only_saves_once(auto_save, mocker):
    """:type mocker: pytest_mock.MockFixture"""
    mocker.spy(auto_save, u'save')

    auto_save['this']['is']['a']['test'] = 'success'
    auto_save['this']['is']['not']['a']['test'] = 'more success'
    auto_save.save.reset_mock()
    assert auto_save.save.call_count == 0

    del auto_save['this']['is']
    assert auto_save.save.call_count == 1


# noinspection PyUnresolvedReferences
def test_deleting_items_actually_saves_updated_value(auto_save, mocker, tmpdir):
    """
    :type auto_save: AutoJSON
    :type mocker: pytest_mock.MockFixture
    :type tmpdir: py._path.local.LocalPath
    """
    config = tmpdir.join(CONFIG)
    mocker.spy(auto_save, u'save')
    auto_save['this']['is']['a']['test'] = 'success'
    auto_save['this']['is']['not']['a']['test'] = 'more success'
    auto_save.save.reset_mock()
    assert auto_save.save.call_count == 0

    with config.open() as f:
        results1 = f.read()
    assert results1 == '{"this": {"is": {"a": {"test": "success"}, "not": {"a": {"test": "more success"}}}}}'

    del auto_save['this']['is']['a']['test']

    with config.open() as f:
        results2 = f.read()
    assert results2 == '{"this": {"is": {"not": {"a": {"test": "more success"}}}}}'
    assert auto_save.save.call_count == 1
    auto_save.save.reset_mock()

    del auto_save['this']['is']

    with config.open() as f:
        results2 = f.read()
    assert results2 == '{}'
    assert auto_save.save.call_count == 1


def test_loading_config_does_not_save_file(mocker, tmpdir):
    """
    :type mocker: pytest_mock.MockFixture
    :type tmpdir: py._path.local.LocalPath
    """
    save = mocker.patch('json_config.main.AutoSyncMixin.save')
    shutil.copytree(dir_tests('sample_assets'), tmpdir.join('sample_assets').strpath)

    auto_load = AutoJSON(config_file=tmpdir.join(SAMPLE_CONFIG_SMALL).strpath)

    assert save.call_count == 0

    auto_load['test'] = 'success'
    assert save.call_count == 1
