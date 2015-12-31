#!/usr/bin/env python
# coding=utf-8

from pytest import fixture


@fixture(autouse=True)
def tear_down(request):
    """:type request: _pytest.python.FixtureRequest"""
    import gc

    # force garbage collection to un register subclasses
    request.addfinalizer(gc.collect)


def test_when_no_file_type_identified_and_no_subclassess_match_defaults_to_json_flavor(tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""
    from json_config.main import connect, PrettyJSONMixin

    config1 = connect(tmpdir.join('config.json').strpath)
    assert isinstance(config1, PrettyJSONMixin)

    config2 = connect(tmpdir.join('.configrc').strpath)
    assert isinstance(config2, PrettyJSONMixin)


def test_custom_flavor_subclasses_automatically_recognized(tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""

    from json_config.contracts import AbstractSerializer
    from json_config.main import connect, PrettyJSONMixin

    class INISerializer(AbstractSerializer):
        serializer_ext = 'ini'

    config = connect(tmpdir.join('config.ini').strpath)
    assert isinstance(config, INISerializer)
    assert not isinstance(config, PrettyJSONMixin)


def test_malformed_serializer_do_not_work(tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""

    from json_config.contracts import AbstractSerializer
    from json_config.main import connect, PrettyJSONMixin

    class INISerializer(AbstractSerializer):
        pass

    config = connect(tmpdir.join('config.ini').strpath)

    assert not isinstance(config, INISerializer)
    assert isinstance(config, PrettyJSONMixin)


def test_custom_serializers_actually_work():
    # TODO
    pass
