"""
Web Services Interface used by command-line clients and web frontend to
view current state, event history and send commands to trond.
"""
import collections
import datetime
import logging

import ujson as json

log = logging.getLogger(__name__)


class LogAdapter(object):
    def __init__(self, logger):
        self.logger = logger

    def write(self, line):
        self.logger.info(line.rstrip(b"\n"))

    def close(self):
        pass


def UltronSite():
    """Web server"""
    pass


class JSONEncoder(json.JSONEncoder):
    """Custom JSON for certain objects"""

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")

        if isinstance(o, datetime.date):
            return o.isoformat()

        if isinstance(o, collections.KeysView):
            return list(o)

        return super(JSONEncoder, self).default(o)
