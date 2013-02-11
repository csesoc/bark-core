# This module forms a wrapper around the standard Python logging module.
# It is not strictly necessary at the moment, but we may extend this later.

__all__ = ['GetLogger']

import logging

def InitLogging():
    """
        Sets up logging facilities.
        Can be called multiple times (with no subsequent effect).
    """

    config = {
        'format': '%(asctime)s %(levelname)s %(name)s: %(message)s',
        'level': logging.NOTSET,
    }

    logging.basicConfig(**config)

# Init logging upon import.
InitLogging()

def GetLogger(name=None):
    return logging.getLogger(name)
