#!/usr/bin/env python
# coding=utf-8
"""The full documentation is at https://json_config.readthedocs.org."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        import sys

        errno = pytest.main(self.test_args)
        sys.exit(errno)


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['future']

test_requirements = ['pytest', 'mock']

setup(  # :off
    name='json_config',
    version='1.2.0',
    description='A convenience utility for working with JSON config files.',
    long_description='\n\n'.join([readme, history]),
    author='Manu Phatak',
    author_email='bionikspoon@gmail.com',
    url='https://github.com/bionikspoon/json_config',
    packages=['json_config',],
    package_dir={'json_config':'json_config'},
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    cmdclass={'test': PyTest},
    keywords='json_config Manu Phatak',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Database',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ],
    test_suite='tests',
    tests_require=test_requirements
)  # :on
