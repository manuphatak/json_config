#!/usr/bin/env python
# coding=utf-8
from json_config.main import AutoDict


# noinspection PyProtectedMember
def test_knows_the_difference_between_a_list_and_not_a_list_when_manually_setting_root():
    sample = AutoDict()
    sample['this']['is']['a']['test'] = 'success'

    expected_obj = {'expected': 'object'}
    sample['this']['is']._root = [expected_obj]

    assert sample['this']['is']._root is expected_obj
