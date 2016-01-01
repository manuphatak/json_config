=====
Usage
=====

To use json_config in a project:

.. code-block:: python

    import json_config

    config = json_config.connect('config.json')
    config['root'] = '/var/www/html/'

    print(config['root'])
    #OUT: '/var/www/html/'
    config
    #OUT:  Connect({'root': '/var/www/html/'})
