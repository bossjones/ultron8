import logging

import requests

from tests.utils.utils import get_server_api
from ultron8.api import settings
import pytest

from typing import Dict

from ultron8 import __version__

logger = logging.getLogger(__name__)


@pytest.mark.convertingtotestclientstarlette
@pytest.mark.loginonly
@pytest.mark.integration
class TestVersionApiEndpoint:
    def test_logger_get(self, fastapi_client):
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        r = fastapi_client.get(f"{server_api}{settings.API_V1_STR}/version")

        cur_version = f"{__version__}"
        content = {"version": cur_version}

        assert r.status_code == 200
        assert r.json() == content
