import logging

import daiquiri

LOGSEVERITY = {
    "CRITICAL": 50,
    "FATAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "WARN": 30,
    "INFO": 20,
    "DEBUG": 10,
    "NOTSET": 0,
}


def setup_logging():
    """Configure logging."""
    daiquiri.setup(level=logging.DEBUG, outputs=(daiquiri.output.STDOUT,))
