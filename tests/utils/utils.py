import logging
import random
import string

import requests

from ultron8.api import settings

from typing import Dict
from starlette.testclient import TestClient

logger = logging.getLogger(__name__)


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_server_api() -> str:
    server_name = f"http://{settings.SERVER_NAME}"
    logger.debug("server_name: '%s'", server_name)
    return server_name


def get_superuser_jwt_request():
    server_api = get_server_api()
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/login/access-token", data=login_data
    )
    return r


def get_superuser_token_headers() -> Dict[str, str]:
    r = get_superuser_jwt_request()
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    # superuser_token_headers = headers
    return headers


superuser_credentials = [
    settings.FIRST_SUPERUSER.encode(),
    settings.FIRST_SUPERUSER_PASSWORD.encode(),
]

# TODO: Figure out if we want to use this or not
def get_superuser_token_headers2(client: TestClient) -> Dict[str, str]:
    """Does basically the same as get_superuser_token_headers() only this time it uses the starlette TestClient

    Arguments:
        client {TestClient} -- [description]

    Returns:
        Dict[str, str] -- [description]
    """
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
