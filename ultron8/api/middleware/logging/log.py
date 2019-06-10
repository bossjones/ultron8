import daiquiri

from ultron8.api import settings

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
    daiquiri.setup(level=settings.LOG_LEVEL, outputs=(daiquiri.output.STDOUT,))
