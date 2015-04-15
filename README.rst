===========
json_config
===========
.. image:: https://travis-ci.org/bionikspoon/json_config.svg?branch=develop
    :target: https://travis-ci.org/bionikspoon/json_config

.. image:: https://pypip.in/version/json_config/badge.svg?branch=develop
    :target: https://pypi.python.org/pypi/json_config?branch=develop

.. image:: https://coveralls.io/repos/bionikspoon/json_config/badge.svg?branch=develop
    :target: https://coveralls.io/r/bionikspoon/json_config?branch=develop

.. image:: https://readthedocs.org/projects/json-config/badge/?version=develop
    :target: https://readthedocs.org/projects/json-config/?badge=develop
    :alt: Documentation Status

A convenience utility for working with JSON configuration files.


Features
--------

* Automatically syncs file on changes
* Automatically handles complicated nested data structures.
* Lightweight (<5KB) and Fast.
* Takes advantage of Python's native dictionary syntax.

.. code-block:: python

    >>> import json_config
    >>> config = json_config.connect('categories.json')
    >>> config
    {}
    >>> config['comics']['dc']['batman']['antagonists'] = ['Scarecrow', 'The Joker', 'Bane']
    >>> config['comics']['marvel']['ironman']['antagonists'] = 'Ultron'
    >>> config
    {
      "comics": {
        "dc": {
          "batman": {
            "antagonists": [
              "Scarecrow",
              "The Joker",
              "Bane"
            ]
          }
        },
        "marvel": {
          "ironman": {
            "antagonists": "Ultron"
          }
        }
      }
    }

Installation
------------

At the command line either via easy_install or pip:

.. code-block:: shell

    $ pip install json_config

.. code-block:: shell

    $ easy_install json_config

**Uninstall**

.. code-block:: shell

    $ pip uninstall json_config


Getting Started
---------------
To use json_config in a project:

.. code-block:: python

    import json_config

    config = json_config.connect('config.json')
    config['root'] = '/var/www/html/'

    print config['root'] # '/var/www/html/'
    print config # { "root": "/var/www/html" }
