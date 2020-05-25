import logging

import pytest
from starlette.testclient import TestClient

from ultron8.api import settings

from tests.utils.utils import get_server_api

logger = logging.getLogger(__name__)


@pytest.mark.convertingtotestclientstarlette
@pytest.mark.integration
class TestHomeApiEndpoint:
    def test_home_get(self, fastapi_client: TestClient) -> None:
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        r = fastapi_client.get(f"{server_api}{settings.API_V1_STR}/")

        content = [{"name": "Item Foo"}, {"name": "item Bar"}]

        assert r.status_code == 200
        assert r.json() == content
