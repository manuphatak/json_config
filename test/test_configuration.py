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
def mock_write_file(empty_config):
    write_file = empty_config.write_file

    empty_config.write_file = Mock(side_effect=write_file)
    # monkeypatch.setattr(empty_config, 'write_file', mock)
    return empty_config


def test_config_file_fixture(sample_config_file):
    json_data = json.load(open(sample_config_file))
    assert json_data['test'] == 'success'


def test_config_file(empty_config_file):
    with pytest.raises(IOError):
        json.load(open(empty_config_file))


def test_loads_json_file_returns_dict_like_obj(config):
    assert config['test'] == 'success'


def test_loads_json_file_returns_dict_like_obj_from_empty(empty_config):
    assert empty_config['test'] == {}


@pytest.mark.skipif
def test_it_returns_the_length_of_all_items_including_children():
    # assert len(config) == 10
    pass  # TODO


def test_it_can_be_iterated_on(config):
    iter_config = list(config)
    assert set(iter_config) == {'test', 'cat_1', 'cat_2', 'cat_3', 'cat_4'}


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
    from json_config.configuration import ConfigObject

    assert isinstance(config['cat_1'], ConfigObject)


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


def test_it_saves_when_a_value_is_set_from_empty(empty_config,
                                                 empty_config_file):
    empty_config['not a test'] = 'mildly pass'
    empty_config.block()
    expected = json.load(open(empty_config_file))

    assert expected['not a test'] == 'mildly pass'


def test_it_saves_only_once_when_a_value_is_set(mock_write_file):
    assert mock_write_file.write_file.call_count == 0
    mock_write_file['not a test'] = 'mildly pass'
    mock_write_file.block()

    assert mock_write_file.write_file.call_count == 1


# @pytest.mark.xfail
def test_it_only_saves_once_when_a_nested_value_is_set(mock_write_file):
    assert mock_write_file.write_file.call_count == 0
    mock_write_file['cat_4'][0]['test']['1']['2']['3'][0] = 'successful 0'
    mock_write_file.block()
    assert mock_write_file.write_file.call_count == 1


def test_it_saves_when_a_value_is_deleted(config, sample_config_file):
    del config['cat_2']
    config.block()

    expected = json.load(open(sample_config_file))

    with pytest.raises(KeyError):
        _ = expected['cat_2']


def test_it_saves_when_a_nested_value_is_set(config, sample_config_file):
    config['cat_3']['sub_2'] = 'test_success'
    assert config['cat_3']['sub_2'] == 'test_success'

    config.block()
    expected = json.load(open(sample_config_file))
    assert expected['cat_3']['sub_2'] == 'test_success'


def test_it_saves_when_a_nested_value_is_set_from_empty(empty_config,
                                                        empty_config_file):
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
    from json_config import configuration

    config = configuration.connect(tmpdir.join('unique_file.json').strpath)

    config['unique'] = 'success'
    config.block()

    actual = json.load((open(tmpdir.join('unique_file.json').strpath)))

    assert actual == dict(config)


@pytest.mark.skipif
def test_it_throws_error_if_nesting_lists_and_dicts():
    # TODO
    pass


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
