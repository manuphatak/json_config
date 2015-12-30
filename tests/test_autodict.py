#!/usr/bin/env python
# coding=utf-8
from json_config.main import AutoDict


def test_compares_as_ordinary_dictionary():
    result = AutoDict()

    assert result == {}


def test_can_be_initialized_with_value():
    sample = {'this is a': 'test'}
    result = AutoDict(sample)

    assert result == sample


def test_can_be_handle_nested():
    sample = AutoDict()

    sample['this']['is']['a']['test'] = 'success'

    assert sample == {'this': {'is': {'a': {'test': 'success'}}}}


def test_knows_its_roots():
    sample = AutoDict()

    sample['this']['is']['a']['test'] = 'success'

    assert sample['this']._is_root == False
    assert sample._is_root == True


def test_can_find_its_root():
    sample = AutoDict()

    sample['this']['is']['a']['test'] = 'success'

    assert sample is sample
    assert sample['this']['is']['a']._root is sample


def test_repr():
    sample1 = AutoDict()
    assert repr(sample1) == 'AutoDict(dict={})'

    sample2 = AutoDict({'this is': 'a test'})
    assert repr(sample2) == "AutoDict(dict={'this is': 'a test'})"

    sample3 = AutoDict()
    sample3['this']['is']['a']['test'] = 'success'

    assert repr(sample3['this']['is']['a']) == repr({'test': 'success'})
