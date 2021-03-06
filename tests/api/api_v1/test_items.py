import logging

import pytest
import requests
from starlette.testclient import TestClient

from ultron8.api import settings

from tests.utils.item import create_random_item
from tests.utils.utils import get_server_api

logger = logging.getLogger(__name__)

# self, mocker: MockFixture, fastapi_client: TestClient, db: Session


@pytest.mark.convertingtotestclientstarlette
@pytest.mark.itemonly
@pytest.mark.integration
@pytest.mark.skip(reason="Flakey Item tests")
class TestLoginApiEndpoint:
    def test_create_item(self, superuser_token_headers, fastapi_client: TestClient):
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        data = {"title": "Foo", "description": "Fighters"}
        response = fastapi_client.post(
            f"{server_api}{settings.API_V1_STR}/items/",
            headers=superuser_token_headers,
            json=data,
        )
        content = response.json()
        assert content["title"] == data["title"]
        assert content["description"] == data["description"]
        assert "id" in content
        assert "owner_id" in content

    def test_read_item(self, db, superuser_token_headers, fastapi_client: TestClient):
        item = create_random_item(db)
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        response = fastapi_client.get(
            f"{server_api}{settings.API_V1_STR}/items/{item.id}",
            headers=superuser_token_headers,
        )
        content = response.json()
        assert content["title"] == item.title
        assert content["description"] == item.description
        assert content["id"] == item.id
        assert content["owner_id"] == item.owner_id
