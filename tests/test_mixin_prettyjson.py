#!/usr/bin/env python
# coding=utf-8
from textwrap import dedent

from pytest import fixture

from json_config.main import PrettyJSONMixin, AutoDict


class Pretty(PrettyJSONMixin, AutoDict):
    pass


@fixture
def pretty():
    _pretty = Pretty()
    _pretty['this']['is']['a']['test'] = 'success'
    _pretty['completely']['different']['tree']['and']['different']['depth'] = 'hello'
    _pretty['this']['is']['not']['a']['test'] = 'more success'
    _pretty['this']['is']['a']['different']['test'] = 'still good'
    return _pretty


def test_can_serialize_a_dict_into_pretty_formatted_json(pretty):
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
    text = dedent("""
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
    # :off
    expected = {'completely': {'different': {'tree': {'and': {'different': {'depth': 'hello'}}}}}, 'this': {'is': {
        'a': {'test': 'success', 'different': {'test': 'still good'}}, 'not': {'a': {'test': 'more success'}}}}}  # :on
    config = Pretty()
    assert config.deserialize(text) == expected


def test_serializer_sanity(pretty):
    serialized1 = pretty.serialize()
    deserialized1 = pretty.deserialize(serialized1)
    pretty.clear()
    pretty.update(deserialized1)
    serialized2 = pretty.serialize()
    deserialized2 = pretty.deserialize(serialized2)

    assert serialized1 == serialized2
    assert deserialized1 == deserialized2
