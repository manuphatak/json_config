#!/usr/bin/env python
# coding=utf-8
import json_config
import os

config = json_config.connect('categories.json')

config['comics']['dc']['batman']['antagonists'] = ['Scarecrow', 'The Joker', 'Bane']
config['comics']['marvel']['ironman']['antagonists'] = 'Ultron'

print(config.serialize())

os.remove('categories.json')
