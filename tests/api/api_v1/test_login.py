import logging

import requests

from tests.utils.utils import get_server_api
from ultron8.api import settings
import pytest

from typing import Dict

logger = logging.getLogger(__name__)


@pytest.mark.convertingtotestclientstarlette
@pytest.mark.loginonly
@pytest.mark.integration
class TestLoginApiEndpoint:
    def test_get_access_token(self, fastapi_client) -> None:
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        login_data = {
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        }
        r = fastapi_client.post(
            f"{server_api}{settings.API_V1_STR}/login/access-token", data=login_data
        )
        tokens = r.json()
        assert r.status_code == 200
        assert "access_token" in tokens
        assert tokens["access_token"]

    @pytest.mark.loginonly
    @pytest.mark.unittest
    def test_use_access_token(
        self, superuser_token_headers: Dict[str, str], fastapi_client
    ) -> None:
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        logger.debug("r = {server_api}{settings.API_V1_STR}/login/test-token")
        r = fastapi_client.post(
            f"{server_api}{settings.API_V1_STR}/login/test-token",
            headers=superuser_token_headers,
        )
        result = r.json()
        assert r.status_code == 200
        assert "email" in result


# @pytest.mark.loginonly
# @pytest.mark.unittest
# def test_get_access_token() -> None:
#     server_api = get_server_api()
#     logger.debug("server_api : %s", server_api)
#     login_data = {
#         "username": settings.FIRST_SUPERUSER,
#         "password": settings.FIRST_SUPERUSER_PASSWORD,
#     }
#     r = requests.post(
#         f"{server_api}{settings.API_V1_STR}/login/access-token", data=login_data
#     )
#     tokens = r.json()
#     assert r.status_code == 200
#     assert "access_token" in tokens
#     assert tokens["access_token"]


# @pytest.mark.loginonly
# @pytest.mark.unittest
# def test_use_access_token(superuser_token_headers: Dict[str, str]) -> None:
#     server_api = get_server_api()
#     logger.debug("server_api : %s", server_api)
#     logger.debug("r = {server_api}{settings.API_V1_STR}/login/test-token")
#     r = requests.post(
#         f"{server_api}{settings.API_V1_STR}/login/test-token",
#         headers=superuser_token_headers,
#     )
#     result = r.json()
#     assert r.status_code == 200
#     assert "email" in result
