#!/usr/bin/env python
# coding=utf-8
from json_config.main import AutoDict


def test_pass_root_as_iterable():
    sample = AutoDict()

    sample['this']['is']['a']['test'] = 'success'

    expected_obj = {'expected': 'object'}

    sample['this']['is']._root = [expected_obj]

    assert sample['this']['is']._root is expected_obj
