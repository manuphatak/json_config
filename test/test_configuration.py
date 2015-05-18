#!/usr/bin/env python
# coding=utf-8
"""
Tests for `configuration` module.
"""
import json
from os.path import dirname, join
import shutil

from mock import Mock
import pytest

test_dir = dirname(__file__)


@pytest.fixture
def sample_config_file(tmpdir):
    config_asset = join(test_dir, 'sample_assets', 'sample_config.json')

    mock_config = tmpdir.join('sample_config.json').strpath
    shutil.copyfile(config_asset, mock_config)
    return mock_config


@pytest.fixture
def config(sample_config_file):
    import json_config

    return json_config.connect(sample_config_file)


@pytest.fixture
def empty_config_file(tmpdir):
    return tmpdir.join('empty_config.json').strpath


@pytest.fixture
def empty_config(empty_config_file):
    import json_config

    return json_config.connect(empty_config_file)


@pytest.fixture
def mock_write(monkeypatch):
    from json_config import configuration

    mock = Mock()

    monkeypatch.setattr(configuration.ConfigObject, 'write_file', mock)
    return mock


def test_config_file_fixture(sample_config_file):
    json_data = json.load(open(sample_config_file))
    assert json_data['test'] == 'success'


def test_loads_json_file_returns_dict_like_obj(config):
    assert config['test'] == 'success'


@pytest.mark.skipif
def test_abc_magic_methods_length():
    # assert len(config) == 10
    pass  # TODO


def test_abc_magic_methods_iter(config):
    iter_config = list(config)
    assert set(iter_config) == {'test', 'cat_1', 'cat_2', 'cat_3', 'cat_4'}


def test_abc_magic_methods_getitem(config):
    assert config['test'] == 'success'


def test_abc_magic_methods_setitem(config):
    config['not a test'] = 'mildly pass'
    assert config['not a test'] == 'mildly pass'


def test_abc_magic_methods_delitem(config):
    del config['test']

    assert config.get('test') is None


def test_loaded_children_are_the_correct_type(config):
    from json_config.configuration import ConfigObject

    assert isinstance(config['cat_1'], ConfigObject)


def test_set_nested_dict(config):
    config['1']['2']['3']['4']['5'] = '6'
    assert config['1']['2']['3']['4']['5'] == '6'


def test_save_on_set(config, sample_config_file):
    config['not a test'] = 'mildly pass'
    expected = json.load(open(sample_config_file))

    assert expected['not a test'] == 'mildly pass'


def test_save_on_delete(config, sample_config_file):
    del config['cat_2']
    expected = json.load(open(sample_config_file))

    with pytest.raises(KeyError):
        _ = expected['cat_2']


def test_saves_on_child_set(config, sample_config_file):
    config['cat_3']['sub_2'] = 'test_success'
    assert config['cat_3']['sub_2'] == 'test_success'

    expected = json.load(open(sample_config_file))
    assert expected['cat_3']['sub_2'] == 'test_success'


def test_saves_on_child_set_empty_config(empty_config, empty_config_file):
    empty_config['cat_3']['sub_2'] = 'test_success'
    assert empty_config['cat_3']['sub_2'] == 'test_success'

    expected = json.load(open(empty_config_file))
    assert expected['cat_3']['sub_2'] == 'test_success'


def test_saves_on_nested_delete(config, sample_config_file):
    del config['test']
    expected = json.load(open(sample_config_file))
    assert expected.get('test') is None


def test_create_new_json_file(tmpdir):
    from json_config import configuration

    config = configuration.connect(tmpdir.join('unique_file.json').strpath)

    config['unique'] = 'success'
    actual = json.load((open(tmpdir.join('unique_file.json').strpath)))

    assert actual == dict(config)


# def test_loads_array_in_object(config):
#     print config['cat_4'][0]
#     assert 0

# @pytest.mark.skipif
# def test_automatically_handles_objects_nested_in_list(config):
#     config['cat_4'][0]['test']['1']['2']['3'][0] = 'successful 0'
#     config['cat_4'][0]['test']['1']['2']['3'][1] = 'successful 1'
#     # print config['cat_4']
#     assert config['cat_4'][0]['test']['1']['2']['3'] == ['successful 0',
#                                                          'successful 1']

@pytest.mark.skipif
def test_throws_error_if_nesting_lists_and_dicts(config):
    # TODO
    pass


def test_multiple_configs(tmpdir, empty_config):
    import json_config

    a = json_config.connect(tmpdir.join('unique_file_a.json').strpath)
    b = json_config.connect(tmpdir.join('unique_file_b.json').strpath)

    a['test'] = 'A success'
    b['test'] = 'B success'
    empty_config['unique'] = 'empty_config success'

    assert a['test'] == 'A success'
    assert b['test'] == 'B success'
    assert a is not b

    a_actual = json.load(open(tmpdir.join('unique_file_a.json').strpath))
    b_actual = json.load(open(tmpdir.join('unique_file_b.json').strpath))
    assert not a_actual == b_actual
    assert a_actual['test'] == 'A success'
    assert b_actual['test'] == 'B success'


def test_save_config_is_only_called_once(config, mock_write):
    assert mock_write.call_count == 0
    config['not a test'] = 'mildly pass'

    assert mock_write.call_count == 1


@pytest.mark.xfail
def test_save_config_is_only_called_once_for_nested_set(config, mock_write):
    assert mock_write.call_count == 0
    config['cat_4'][0]['test']['1']['2']['3'][0] = 'successful 0'

    assert mock_write.call_count == 1
