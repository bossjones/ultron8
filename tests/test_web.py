"""Test Web Module."""
# pylint: disable=protected-access
import logging

from fastapi.applications import FastAPI
import pytest
from pytest_mock.plugin import MockFixture
from starlette.testclient import TestClient

import ultron8
from ultron8.api import settings

# from ultron8 import __version__
# from ultron8 import client
from tests.utils.utils import get_server_api_with_version

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def username_and_password_first_superuser_fixtures():
    yield settings.FIRST_SUPERUSER, settings.FIRST_SUPERUSER_PASSWORD


@pytest.mark.fastapionly
@pytest.mark.unittest
class TestFastAPIWeb:
    def test_fastapi_instance(
        self, mocker: MockFixture, fastapi_client: TestClient
    ) -> None:
        # username, password = username_and_password_first_superuser_fixtures
        url = "{base}/logs".format(base=get_server_api_with_version())
        response = fastapi_client.get(url)
        assert response.status_code == 200

    def test_fastapi_app_instance(
        self, mocker: MockFixture, fastapi_app: FastAPI, fastapi_client: TestClient
    ) -> None:
        # username, password = username_and_password_first_superuser_fixtures
        assert fastapi_app.title == "Ultron-8 Web Server"
        assert fastapi_app.debug
        assert fastapi_app.description == ""
        url = "{base}/logs".format(base=get_server_api_with_version())
        response = fastapi_client.get(url)
        assert response.status_code == 200

    def test_fastapi_app_routes(
        self, mocker: MockFixture, fastapi_app: FastAPI, fastapi_client: TestClient
    ) -> None:
        routes = {}
        for r in fastapi_app.router.routes:
            routes[r.path] = r
        print(routes)
        print(fastapi_app)
        expected_routes = [
            "/openapi.json",
            "/docs",
            "/docs/oauth2-redirect",
            "/redoc",
            "/v1/metrics",
            "/v1/logs/",
            "/v1/token",
            "/v1/alive",
            "/v1/version",
            "/v1/login/access-token",
            "/v1/login/test-token",
            "/v1/login/test-token",
        ]

        for i in expected_routes:
            assert routes[i]
