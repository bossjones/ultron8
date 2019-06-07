import logging

import daiquiri


def setup_logging():
    """Configure logging."""
    daiquiri.setup(level=logging.DEBUG, outputs=(daiquiri.output.STDOUT,))
