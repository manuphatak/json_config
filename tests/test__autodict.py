#!/usr/bin/env python
# coding=utf-8
from json_config.main import AutoDict


def test_quacks_like_an_ordinary_dict():
    result = AutoDict()

    assert result == {}


def test_can_be_initialized_with_value():
    sample = {'this is a': 'test'}
    result = AutoDict(obj=sample)

    assert result == sample


def test_automatically_creates_nested_dict():
    sample = AutoDict()

    sample['this']['is']['a']['test'] = 'success'

    assert sample == {'this': {'is': {'a': {'test': 'success'}}}}


def test_repr_offers_some_reasonable_output():
    sample1 = AutoDict()
    assert repr(sample1) == 'AutoDict({})'

    sample2 = AutoDict({'this is': 'a test'})
    assert repr(sample2) == "AutoDict({'this is': 'a test'})"

    sample3 = AutoDict()
    sample3['this']['is']['a']['test'] = 'success'

    assert repr(sample3['this']['is']['a']) == repr({'test': 'success'})


def test_values_can_be_updated_without_replacing_the_entire_tree():
    sample = AutoDict()

    sample['this']['is']['a']['test'] = 'success'
    sample['this']['is']['not']['a']['test'] = 'more success'
    sample['this']['is']['a']['different']['test'] = 'still good'

    expected = {  # :off
        'this': {
            'is': {
                'a': {
                    'different': {
                        'test': 'still good'
                    },
                    'test': 'success'
                },
                'not': {
                    'a': {
                        'test': 'more success'
                    }
                }
            }
        }
    }  # :on

    assert sample == expected


def test_setting_an_empty_dict_does_not_break_flow():
    sample1 = AutoDict()

    sample1['this'] = {}
    sample1['this']['is']['a']['test'] = 'success'

    assert sample1['this']['is']['a']['test'] == 'success'

    sample2 = AutoDict()

    sample2['this'] = {'is another potential': 'edge'}
    sample2['this']['is']['a']['test'] = 'success'

    expected = {  # :off
        'this': {
            'is another potential': 'edge',
            'is': {
                'a': {
                    'test': 'success'
                }
            }
        }
    }  # :on

    assert sample2 == expected


def test_setting_a_list_does_no_break_flow():
    # TODO
    pass


def test_items_can_be_deleted():
    sample1 = AutoDict()

    sample1['this']['is']['a']['test'] = 'success'
    del sample1['this']['is']['a']['test']
    assert sample1 == {}

    sample2 = AutoDict()

    sample2['this']['is']['a']['test'] = 'success'
    sample2['this']['is']['not']['a']['test'] = 'more success'
    del sample2['this']['is']['a']
    # :off
    assert sample2 == {'this': {'is': {'not': {'a': {'test': 'more success'}}}}}  # :on


def test_deleted_leafs_also_remove_branch():
    sample = AutoDict()

    sample['this']['is']['a']['test'] = 'success'
    sample['this']['is']['not']['a']['test'] = 'more success'
    del sample['this']['is']
    assert sample == {}
