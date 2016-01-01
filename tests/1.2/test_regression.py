#!/usr/bin/env python
# coding=utf-8
"""
Tests for `configuration` module.
"""
import json
import shutil
from functools import partial

import os
from pytest import fixture, raises
from warnings import warn


def dir_tests(*paths):
    dirname = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(dirname, *paths))


warn_depreciated = partial(warn, 'Removed after 1.2', DeprecationWarning)


@fixture(autouse=True)
def patched_connect(monkeypatch):
    """:type monkeypatch: _pytest.monkeypatch.monkeypatch"""
    from json_config.main import AutoSyncMixin, AutoDict, connect

    # noinspection PyAbstractClass,PyMethodMayBeStatic
    class MockAutoConfigBase(AutoSyncMixin, AutoDict):
        def __init__(self, config_file=None, **kwargs):
            # normalize kwargs
            kwargs.setdefault('config_file', config_file)
            super(MockAutoConfigBase, self).__init__(**kwargs)

        # Internally used api
        def block(self):
            warn_depreciated()

        # Internally used api
        def write_file(self):
            warn_depreciated()

        # bridge old api
        def save(self):
            super(MockAutoConfigBase, self).save()
            self.write_file()

    if not hasattr(connect, 'block') or not hasattr(connect, 'write_file'):
        monkeypatch.setattr('json_config.main.AutoConfigBase', MockAutoConfigBase)
    return connect


@fixture
def sample_config_file(tmpdir):
    config_asset = dir_tests('sample_assets', 'sample_config.json')

    mock_config = tmpdir.join('sample_config.json').strpath
    shutil.copyfile(config_asset, mock_config)
    return mock_config


@fixture
def config(patched_connect, sample_config_file):
    return patched_connect(sample_config_file)


@fixture
def empty_config_file(tmpdir):
    return tmpdir.join('empty_config.json').strpath


@fixture
def empty_config(patched_connect, empty_config_file):
    return patched_connect(empty_config_file)


def test_config_file_fixture(sample_config_file):
    json_data = json.load(open(sample_config_file))
    assert json_data['test'] == 'success'


def test_config_file(empty_config_file):
    with raises(IOError):
        json.load(open(empty_config_file))


def test_loads_json_file_returns_dict_like_obj(config):
    assert config['test'] == 'success'


def test_loads_json_file_returns_dict_like_obj_from_empty(empty_config):
    assert empty_config['test'] == {}


def test_it_can_be_iterated_on(config):
    iter_config = list(config)
    assert set(iter_config) == set(['test', 'cat_1', 'cat_2', 'cat_3', 'cat_4'])


def test_it_uses_dictionary_syntax_for_get(config):
    assert config['test'] == 'success'


def test_it_uses_dictionary_syntax_for_set(config):
    config['not a test'] = 'mildly pass'
    assert config['not a test'] == 'mildly pass'


def test_it_uses_dictionary_syntax_for_set_from_empty(empty_config):
    empty_config['not a test'] = 'mildly pass'
    assert empty_config['not a test'] == 'mildly pass'


def test_it_uses_dictionary_syntax_for_deletions(config):
    del config['test']

    assert config.get('test') is None


def test_it_uses_dictionary_syntax_for_deletions_from_empty(empty_config):
    empty_config['test'] = 'Ahoy'
    assert empty_config['test'] == 'Ahoy'

    del empty_config['test']

    assert empty_config.get('test') is None


def test_nodes_are_being_loaded_into_config_object(config):
    from json_config.main import AutoSyncMixin

    assert isinstance(config['cat_1'], AutoSyncMixin)


def test_it_can_recursively_create_dictionaries(config):
    config['1']['2']['3']['4']['5'] = '6'
    assert config['1']['2']['3']['4']['5'] == '6'


def test_it_can_recursively_create_dictionaries_from_empty(empty_config):
    empty_config['1']['2']['3']['4']['5'] = '6'
    assert empty_config['1']['2']['3']['4']['5'] == '6'


def test_it_saves_when_a_value_is_set(config, sample_config_file):
    config['not a test'] = 'mildly pass'
    config.block()

    expected = json.load(open(sample_config_file))

    assert expected['not a test'] == 'mildly pass'


def test_it_saves_when_a_value_is_set_from_empty(empty_config, empty_config_file):
    empty_config['not a test'] = 'mildly pass'
    empty_config.block()
    expected = json.load(open(empty_config_file))

    assert expected['not a test'] == 'mildly pass'


def test_it_saves_only_once_when_a_value_is_set(empty_config, mocker):
    mocker.spy(empty_config, u'write_file')
    assert empty_config.write_file.call_count == 0
    empty_config['not a test'] = 'mildly pass'
    empty_config.block()

    assert empty_config.write_file.call_count == 1


def test_it_only_saves_once_when_a_nested_value_is_set(empty_config, mocker):
    mocker.spy(empty_config, u'write_file')
    assert empty_config.write_file.call_count == 0
    empty_config['cat_4'][0]['test']['1']['2']['3'][0] = 'successful 0'
    empty_config.block()
    assert empty_config.write_file.call_count == 1


def test_it_saves_when_a_value_is_deleted(config, sample_config_file):
    del config['cat_2']
    config.block()

    expected = json.load(open(sample_config_file))

    with raises(KeyError):
        _ = expected['cat_2']  # noqa


def test_it_saves_when_a_nested_value_is_set(config, sample_config_file):
    config['cat_3']['sub_2'] = 'test_success'
    assert config['cat_3']['sub_2'] == 'test_success'

    config.block()
    expected = json.load(open(sample_config_file))
    assert expected['cat_3']['sub_2'] == 'test_success'


def test_it_saves_when_a_nested_value_is_set_from_empty(empty_config, empty_config_file):
    empty_config['cat_3']['sub_2'] = 'test_success'

    assert empty_config['cat_3']['sub_2'] == 'test_success'

    assert empty_config.config_file == empty_config_file
    empty_config.block()
    expected = json.load(open(empty_config_file))
    assert expected['cat_3']['sub_2'] == 'test_success'


def test_it_saves_when_a_nested_value_is_deleted(config, sample_config_file):
    del config['test']
    config.block()

    expected = json.load(open(sample_config_file))
    assert expected.get('test') is None


def test_it_creates_a_new_file(tmpdir):
    from json_config import connect

    config = connect(tmpdir.join('unique_file.json').strpath)

    config['unique'] = 'success'
    config.block()

    actual = json.load((open(tmpdir.join('unique_file.json').strpath)))

    assert actual == dict(config)


def test_it_can_handle_multiple_config_files(tmpdir, empty_config):
    import json_config

    a = json_config.connect(tmpdir.join('unique_file_a.json').strpath)
    b = json_config.connect(tmpdir.join('unique_file_b.json').strpath)

    a['test'] = 'A success'
    b['test'] = 'B success'
    empty_config['unique'] = 'empty_config success'

    assert a['test'] == 'A success'
    assert b['test'] == 'B success'
    assert a is not b

    empty_config.block()
    a.block()
    b.block()

    a_actual = json.load(open(tmpdir.join('unique_file_a.json').strpath))
    b_actual = json.load(open(tmpdir.join('unique_file_b.json').strpath))
    assert not a_actual == b_actual
    assert a_actual['test'] == 'A success'
    assert b_actual['test'] == 'B success'
