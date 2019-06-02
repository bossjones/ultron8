"""
Web Services Interface used by command-line clients and web frontend to
view current state, event history and send commands to trond.
"""

import logging

log = logging.getLogger(__name__)

class LogAdapter(object):
    def __init__(self, logger):
        self.logger = logger

    def write(self, line):
        self.logger.info(line.rstrip(b'\n'))

    def close(self):
        pass


def UltronSite():
    """Web server"""
    pass
