Features
--------

- Documentation: https://json_config.readthedocs.org
- Open Source: https://github.com/bionikspoon/json_config
- MIT license

..

- Automatically syncs file on changes.
- Automatically handles complicated nested data structures.
- Designed to be easily extended.  Use different serializer libraries to easily switch to yaml, ini, etc.
- Lightweight (<5KB) and Fast.
- Takes advantage of Python's native dictionary syntax.
- Tested against python 2.6, 2.7, 3.3, 3.4, 3.5, and PYPY!
- Unit Tested with high coverage.
- Idiomatic, self-descriptive code & api

.. code-block:: python

    >>> import json_config
    >>> config = json_config.connect('categories.json')
    >>> config
    Connect({})
    >>> config['comics']['dc']['batman']['antagonists'] = ['Scarecrow', 'The Joker', 'Bane']
    >>> config['comics']['marvel']['ironman']['antagonists'] = 'Ultron'
    >>> print(config.serialize())
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

