#!/usr/bin/env python
# coding=utf-8
from textwrap import dedent

from pytest import fixture

from json_config.main import PrettyJSONMixin, AutoDict


@fixture
def pretty():
    class Pretty(PrettyJSONMixin, AutoDict):
        pass

    _pretty = Pretty()
    _pretty['this']['is']['a']['test'] = 'success'
    _pretty['completely']['different']['tree']['and']['different']['depth'] = 'hello'
    _pretty['this']['is']['not']['a']['test'] = 'more success'
    _pretty['this']['is']['a']['different']['test'] = 'still good'
    return _pretty


def test_can_serialize_dict(pretty):
    expected = dedent("""
        {
          "completely": {
            "different": {
              "tree": {
                "and": {
                  "different": {
                    "depth": "hello"
                  }
                }
              }
            }
          },
          "this": {
            "is": {
              "a": {
                "different": {
                  "test": "still good"
                },
                "test": "success"
              },
              "not": {
                "a": {
                  "test": "more success"
                }
              }
            }
          }
        }
        """)[1:-1]

    assert pretty.serialize() == expected


def test_serialize_with_different_indent(pretty):
    expected = dedent("""
        {
            "completely": {
                "different": {
                    "tree": {
                        "and": {
                            "different": {
                                "depth": "hello"
                            }
                        }
                    }
                }
            },
            "this": {
                "is": {
                    "a": {
                        "different": {
                            "test": "still good"
                        },
                        "test": "success"
                    },
                    "not": {
                        "a": {
                            "test": "more success"
                        }
                    }
                }
            }
        }
        """)[1:-1]

    assert pretty.serialize(indent=4) == expected

def test_can_deserialize_json_data():
    # TODO
    pass

def test_serializer_sanity():
    # TODO
    pass
