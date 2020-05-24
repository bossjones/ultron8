# pylint: disable=logging-not-lazy
import logging

from ultron8.api import settings

logger = logging.getLogger(__name__)


def get_api_endpoint() -> str:
    server_name = f"http://{settings.SERVER_NAME}"
    logger.debug("server_name: '%s'", server_name)
    return server_name
