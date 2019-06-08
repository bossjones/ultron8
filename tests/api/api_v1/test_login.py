import logging
import requests

from ultron8.api import settings
from tests.utils.utils import get_server_api

logger = logging.getLogger(__name__)

def test_get_access_token():
    server_api = get_server_api()
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/login/access-token", data=login_data
    )
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_use_access_token(superuser_token_headers):
    server_api = get_server_api()
    logger.debug("r = {server_api}{settings.API_V1_STR}/login/test-token",)
    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/login/test-token",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result
