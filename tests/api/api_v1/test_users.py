import logging

import requests

from tests.utils.user import user_authentication_headers
from tests.utils.utils import get_server_api
from tests.utils.utils import random_lower_string, random_email
from ultron8.api import crud
from ultron8.api import settings
from ultron8.api.db.u_sqlite.session import db_session
from ultron8.api.models.user import UserCreate
import pytest
from ultron8.api.factories.users import _MakeRandomNormalUserFactory

from typing import Dict

logger = logging.getLogger(__name__)


@pytest.mark.usersonly
@pytest.mark.unittest
def test_get_users_superuser_me(superuser_token_headers: Dict[str, str]) -> None:
    server_api = get_server_api()
    logger.debug("server_api : %s", server_api)
    r = requests.get(
        f"{server_api}{settings.API_V1_STR}/users/me", headers=superuser_token_headers
    )
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


@pytest.mark.usersonly
@pytest.mark.unittest
def test_create_user_new_email(superuser_token_headers: Dict[str, str]) -> None:
    server_api = get_server_api()
    logger.debug("server_api : %s", server_api)
    username = random_lower_string()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_email(db_session, email=username)
    assert user.email == created_user["email"]


# @pytest.mark.fastapionly
# @pytest.mark.unittest
# class TestFastAPIWeb:
#     def test_fastapi_instance(self, mocker, fastapi_client):
#         # username, password = username_and_password_first_superuser_fixtures
#         url = "{base}/logs".format(base=get_server_api_with_version())
#         response = fastapi_client.get(url)
#         assert response.status_code == 200

#     def test_fastapi_app_instance(self, mocker, fastapi_app, fastapi_client):
#         # username, password = username_and_password_first_superuser_fixtures
#         assert fastapi_app.title == "Ultron-8 Web Server"
#         assert fastapi_app.debug
#         assert fastapi_app.description == ""
#         url = "{base}/logs".format(base=get_server_api_with_version())
#         response = fastapi_client.get(url)
#         assert response.status_code == 200


@pytest.mark.usersonly
@pytest.mark.unittest
def test_get_existing_user(superuser_token_headers: Dict[str, str]) -> None:
    server_api = get_server_api()
    logger.debug("server_api : %s", server_api)
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db_session, user_in=user_in)
    user_id = user.id
    r = requests.get(
        f"{server_api}{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    user = crud.user.get_by_email(db_session, email=username)
    assert user.email == api_user["email"]


@pytest.mark.usersonly
@pytest.mark.unittest
def test_create_user_existing_username(superuser_token_headers: Dict[str, str]) -> None:
    server_api = get_server_api()
    logger.debug("server_api : %s", server_api)
    username = random_lower_string()
    # username = email
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db_session, user_in=user_in)
    data = {"email": username, "password": password}
    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


@pytest.mark.usersonly
@pytest.mark.unittest
def test_create_user_by_normal_user() -> None:
    server_api = get_server_api()
    logger.debug("server_api : %s", server_api)
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db_session, user_in=user_in)
    user_token_headers = user_authentication_headers(server_api, username, password)
    data = {"email": username, "password": password}
    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/users/",
        headers=user_token_headers,
        json=data,
    )
    assert r.status_code == 400


@pytest.mark.usersonly
@pytest.mark.unittest
def test_retrieve_users(superuser_token_headers: Dict[str, str]) -> None:
    server_api = get_server_api()
    logger.debug("server_api : %s", server_api)
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db_session, user_in=user_in)

    username2 = random_lower_string()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    user2 = crud.user.create(db_session, user_in=user_in2)

    r = requests.get(
        f"{server_api}{settings.API_V1_STR}/users/", headers=superuser_token_headers
    )
    all_users = r.json()

    assert len(all_users) > 1
    for user in all_users:
        assert "email" in user


@pytest.mark.convertingtotestclientstarlette
@pytest.mark.usersonly
@pytest.mark.unittest
class TestUserApiEndpoint:
    def test_create_user_new_email_with_starlette_client(
        self, superuser_token_headers: Dict[str, str], mocker, fastapi_client
    ) -> None:
        # SOURCE: https://github.com/tiangolo/fastapi/issues/300
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)

        data = _MakeRandomNormalUserFactory()
        print(data)
        # # email = random_email()
        # # password = random_lower_string()
        # # data = UserCreate(
        # #     email=email,
        # #     password=password
        # # )
        r = fastapi_client.post(
            f"{server_api}{settings.API_V1_STR}/users/",
            headers=superuser_token_headers,
            json=data.dict(),
        )
        assert 200 <= r.status_code < 300
        created_user = r.json()
        user = crud.user.get_by_email(db_session, email=data.email)
        assert user.email == created_user["email"]

        logger.debug(r)
        logger.debug(r.reason)
        logger.debug(r.text)
