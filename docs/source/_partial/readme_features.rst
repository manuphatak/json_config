Features
--------

- Documentation: https://json_config.readthedocs.org
- Open Source: https://github.com/bionikspoon/json_config
- MIT license

..

- Automatically syncs file on changes.
- Automatically handles complicated nested data structures.
- Lightweight (<5KB) and Fast.
- Takes advantage of Python's native dictionary syntax.
- Tested against python 2.7, 3.2, 3.3, 3.4, and PYPY.
- Saves silently in the background.
- Unit Tested with high coverage.

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
