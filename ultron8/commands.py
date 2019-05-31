from . import cli
from .logging import getLogger

logger = getLogger(__name__)


def info() -> None:
    """Get Info on Ultron"""
    logger.info("Ultron8 is running")
