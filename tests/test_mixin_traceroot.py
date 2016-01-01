#!/usr/bin/env python
# coding=utf-8
from json_config.main import AutoDict


# noinspection PyProtectedMember
def test_knows_its_roots():
    sample = AutoDict()

    sample['this']['is']['a']['test'] = 'success'

    assert sample['this']._is_root is False
    assert sample._is_root is True


# noinspection PyProtectedMember
def test_can_find_its_root():
    sample = AutoDict()

    sample['this']['is']['a']['test'] = 'success'

    assert sample is sample
    assert sample['this']['is']['a']._root is sample
