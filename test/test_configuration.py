#!/usr/bin/env python
# coding=utf-8
"""
Tests for `configuration` module.
"""
import json
from os.path import dirname, join
import shutil

import pytest


test_dir = dirname(__file__)


@pytest.fixture
def config_file(tmpdir):
    config_asset = join(test_dir, 'sample_assets', 'sample_config.json')

    mock_config = tmpdir.join('sample_config.json').strpath
    shutil.copyfile(config_asset, mock_config)
    return mock_config


@pytest.fixture
def config(config_file):
    from json_config import configuration

    return configuration.connect(config_file)


def test_config_file_fixture(config_file):
    json_data = json.load(open(config_file))
    assert json_data['test'] == 'success'


def test_loads_json_file_returns_dict_like_obj(config, tmpdir):
    from json_config import configuration

    assert config['test'] == 'success'
    assert configuration.config_file == tmpdir.join('sample_config.json').strpath


def test_abc_magic_methods_length():
    # assert len(config) == 10
    pass  # TODO


def test_abc_magic_methods_iter(config):
    iter_config = list(config)
    assert set(iter_config) == {'test', 'cat_1', 'cat_2', 'cat_3'}


def test_abc_magic_methods_getitem(config):
    assert config['test'] == 'success'


def test_abc_magic_methods_setitem(config):
    config['not a test'] = 'mildly pass'
    assert config['not a test'] == 'mildly pass'


def test_abc_magic_methods_delitem(config):
    del config['test']

    assert config.get('test') is None


def test_loaded_children_are_the_correct_type(config):
    from json_config.configuration import Configuration

    assert isinstance(config['cat_1'], Configuration)


def test_set_nested_dict(config):
    config['1']['2']['3']['4']['5'] = '6'
    assert config['1']['2']['3']['4']['5'] == '6'


def test_save_on_set(config, config_file):
    config['not a test'] = 'mildly pass'
    expected = json.load(open(config_file))

    assert expected['not a test'] == 'mildly pass'


def test_save_on_delete(config, config_file):
    del config['cat_2']
    expected = json.load(open(config_file))

    with pytest.raises(KeyError):
        _ = expected['cat_2']


def test_saves_on_child_set(config, config_file):
    config['cat_3']['sub_2'] = 'test_success'
    expected = json.load(open(config_file))
    assert expected['cat_3']['sub_2'] == 'test_success'


def test_saves_on_nested_delete(config, config_file):
    del config['test']
    expected = json.load(open(config_file))
    assert expected.get('test') is None


def test_create_new_json_file(tmpdir):
    from json_config import configuration

    config = configuration.connect(tmpdir.join('unique_file.json').strpath)

    config['unique'] = 'success'
    actual = json.load((open(tmpdir.join('unique_file.json').strpath)))

    assert actual == dict(config)
