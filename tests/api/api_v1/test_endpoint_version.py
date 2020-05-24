import logging

from typing import Dict

import pytest
import requests
from starlette.testclient import TestClient

from ultron8 import __version__
from ultron8.api import settings

from tests.utils.utils import get_server_api

logger = logging.getLogger(__name__)


@pytest.mark.convertingtotestclientstarlette
@pytest.mark.loginonly
@pytest.mark.integration
class TestVersionApiEndpoint:
    def test_logger_get(self, fastapi_client: TestClient) -> None:
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        r = fastapi_client.get(f"{server_api}{settings.API_V1_STR}/version")

        cur_version = f"{__version__}"
        content = {"version": cur_version}

        assert r.status_code == 200
        assert r.json() == content
