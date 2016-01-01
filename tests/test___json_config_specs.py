#!/usr/bin/env python
# coding=utf-8
import json
import shutil
from textwrap import dedent

from future.utils import PY2, PY3
from pytest import fixture

from tests.utils import dir_tests


def test_readme_example(tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""
    import json_config

    config = json_config.connect(tmpdir.join('categories.json').strpath)
    assert repr(config) == 'Connect({})'

    config['comics']['dc']['batman']['antagonists'] = ['Scarecrow', 'The Joker', 'Bane']
    config['comics']['marvel']['ironman']['antagonists'] = 'Ultron'

    serialize_expected = dedent("""
        {
          "comics": {
            "dc": {
              "batman": {
                "antagonists": [
                  "Scarecrow",
                  "The Joker",
                  "Bane"
                ]
              }
            },
            "marvel": {
              "ironman": {
                "antagonists": "Ultron"
              }
            }
          }
        }
    """)[1:-1]

    assert (config.serialize()) == serialize_expected

    with tmpdir.join('categories.json').open() as f:
        written = f.read()

    assert written == serialize_expected


def test_usage_example(tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""
    import json_config

    config = json_config.connect(tmpdir.join('config.json').strpath)
    config['root'] = '/var/www/html/'

    assert str(config['root']) == '/var/www/html/'
    assert repr(config['root']) == "'/var/www/html/'"

    assert repr(config) == "Connect({'root': '/var/www/html/'})"

    with tmpdir.join('config.json').open() as f:
        written = f.read()

    expected = dedent("""
        {
          "root": "/var/www/html/"
        }
    """)[1:-1]

    assert written == expected


@fixture
def basic_config(tmpdir, mocker):
    """
    :type tmpdir: py._path.local.LocalPath
    :type mocker: pytest_mock.MockFixture
    """
    import json_config

    config = json_config.connect(tmpdir.join('basic_config.json').strpath)
    mocker.spy(config, u'save')
    return config


def test_it_can_recursively_create_dicts(basic_config):
    """:type basic_config: json_config.connect"""
    basic_config['1']['2']['3']['4']['5'] = '6'
    assert basic_config['1']['2']['3']['4']['5'] == '6'
    assert basic_config.save.call_count == 1


def test_it_can_recursively_update_nested_dicts(basic_config):
    """:type basic_config: json_config.connect"""
    basic_config['1']['2']['3']['4']['5'] = '6'
    basic_config['1']['2']['7']['8']['9'] = '10'

    assert basic_config['1']['2']['7']['8']['9'] == '10'
    assert basic_config.save.call_count == 2


def test_new_objects_are_not_regular_dicts(basic_config):
    """:type basic_config: json_config.connect"""
    basic_config['1']['2']['3']['4']['5'] = '6'

    if PY3:
        assert str(type(basic_config)) == "<class 'json_config.main.connect.<locals>.Connect'>"
        assert str(type(basic_config['1']['2'])) == "<class 'json_config.main.connect.<locals>.Connect'>"
    if PY2:
        assert str(type(basic_config)) == "<class 'json_config.main.Connect'>"
        assert str(type(basic_config['1']['2'])) == "<class 'json_config.main.Connect'>"


def test_deleting_keys_save_file(basic_config, tmpdir):
    """
    :type basic_config: json_config.connect
    :type tmpdir: py._path.local.LocalPath
    """
    basic_config.serializer_indent = None
    basic_config['1']['2']['3']['4']['5'] = '6'
    basic_config['1']['2']['3']['4']['7'] = '8'
    assert basic_config.save.call_count == 2

    del basic_config['1']['2']['3']['4']['5']
    assert basic_config.save.call_count == 3

    with tmpdir.join('basic_config.json').open() as f:
        written = f.read()
    assert written == '{"1": {"2": {"3": {"4": {"7": "8"}}}}}'


def test_deleting_nested_keys_save_file(basic_config, tmpdir):
    """
    :type basic_config: json_config.connect
    :type tmpdir: py._path.local.LocalPath
    """
    basic_config['1']['2']['3']['4']['5'] = '6'
    assert basic_config.save.call_count == 1

    del basic_config['1']['2']
    assert basic_config.save.call_count == 2

    with tmpdir.join('basic_config.json').open() as f:
        written = f.read()
    assert written == '{}'


def test_it_can_serialize_data(basic_config):
    """:type basic_config: json_config.connect"""
    basic_config.serializer_indent = None
    basic_config['1']['2']['3']['4']['5'] = '6'
    assert basic_config.serialize() == '{"1": {"2": {"3": {"4": {"5": "6"}}}}}'


def test_it_can_deserialize_data(basic_config):
    """:type basic_config: json_config.connect"""
    result = basic_config.deserialize('{"1": {"2": {"3": {"4": {"5": "6"}}}}}')
    # :off
    assert result == {"1": {"2": {"3": {"4": {"5": "6"}}}}}  # :on


@fixture
def loaded_config(tmpdir, mocker):
    """
    :type tmpdir: py._path.local.LocalPath
    :type mocker: pytest_mock.MockFixture
    """
    import json_config

    config_asset = dir_tests('sample_assets', 'sample_config_small.json')

    loaded_config_file = tmpdir.join('sample_config_small.json')
    shutil.copyfile(config_asset, loaded_config_file.strpath)

    config = json_config.connect(loaded_config_file.strpath)
    mocker.spy(config, u'save')
    return config


def test_loaded_config_setup(loaded_config):
    """:type loaded_config: json_config.connect"""
    assert loaded_config.save.call_count == 0
    assert loaded_config['test'] == 'success'


def test_loaded_objects_save_on_set(loaded_config, tmpdir):
    """
    :type loaded_config: json_config.connect
    :type tmpdir: py._path.local.LocalPath
    """
    loaded_config['test'] = 'more success'
    assert loaded_config.save.call_count == 1

    with tmpdir.join('sample_config_small.json').open() as f:
        written = json.load(f)

    assert loaded_config == written
    assert written['test'] == loaded_config['test'] == 'more success'


def test_it_can_handle_multiple_instances_without_clashing(tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""
    import json_config

    a_path = tmpdir.join('unique_file_a.json')
    b_path = tmpdir.join('unique_file_b.json')

    a = json_config.connect(a_path.strpath)
    b = json_config.connect(b_path.strpath)

    a['test'] = 'A success'
    b['test'] = 'B success'

    assert a['test'] == 'A success'
    assert b['test'] == 'B success'
    assert a is not b

    with a_path.open() as f:
        a_written = f.read()
    with b_path.open() as f:
        b_written = f.read()

    assert a_written != b_written
    assert a_written == '{\n  "test": "A success"\n}'
    assert b_written == '{\n  "test": "B success"\n}'


def test_it_can_be_extended_with_custom_serializers():
    # TODO
    pass
