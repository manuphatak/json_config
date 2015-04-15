#!/usr/bin/env python
# coding=utf-8

"""
Documentation
-------------

The full documentation is at https://json-config.readthedocs.org.
"""
import os
import sys
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools.command.test import test as TestCommand

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.test_args)
        sys.exit(errno)


_version_re = re.compile(r"(?<=^__version__ = \')[\w\.]+(?=\'$)", re.U | re.M)
with open('json_config/__init__.py', 'rb') as f:
    version = _version_re.search(f.read().decode('utf-8')).group()
with open('README.rst') as f:
    readme = f.read()
with open('HISTORY.rst') as f:
    history = f.read().replace('.. :changelog:', '')


# @:off
setup(
    name='json_config',
    version=version,
    description='A convenience utility for working with JSON config files.',
    long_description=readme + '\n\n' + __doc__ + '\n\n' + history,
    author='Manu Phatak',
    author_email='bionikspoon@gmail.com',
    url='https://github.com/bionikspoon/json_config',
    keywords='json config',
    packages=[
        'json_config',
    ],
    package_dir={'json_config': 'json_config'},
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False,
    cmdclass={'test': PyTest},
    tests_require=['pytest', 'mock'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Database',
        'Topic :: Software Development',
        'Topic :: Utilities'


    ],
)
# @:on
