#!/usr/bin/env python
# coding=utf-8
"""
===========
JSON Config
===========
A convenience utility for working with json config files.

>>> import json_config
>>> config = json_config.connect('test.json')
>>> config['root'] = '/var/www/html'
>>> config
{
  "root": "/var/www/html"
}

"""
__author__ = 'Manu Phatak'
__email__ = 'bionikspoon@gmail.com'
__version__ = '1.1.0'

from .configuration import connect