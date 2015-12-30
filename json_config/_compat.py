# coding=utf-8
"""Python 2to3 compatibility handling."""

import logging
from future.utils import PY26, PY2, PY3

__all__ = ['NullHandler', 'FileNotFoundError']

if not PY26:
    from logging import NullHandler
else:  # pragma: no cover
    # Python < 2.7
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

if PY2:
    FileNotFoundError = IOError
elif PY3:
    # noinspection PyUnresolvedReferences,PyCompatibility
    from builtins import FileNotFoundError
