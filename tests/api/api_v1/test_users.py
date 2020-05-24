import logging

import requests

from tests.utils.user import user_authentication_headers
from tests.utils.utils import get_server_api
from tests.utils.utils import random_lower_string, random_email
from ultron8.api import crud
from ultron8.api import settings

from ultron8.api.models.user import UserCreate
from ultron8.api.models.user import UserUpdate
import pytest
from ultron8.api.factories.users import _MakeRandomNormalUserFactory
from ultron8.api.api_v1.endpoints import users
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from typing import Callable, Iterator, Dict
from _pytest.fixtures import SubRequest
from _pytest.monkeypatch import MonkeyPatch
from pytest_mock.plugin import MockFixture
from sqlalchemy.orm.session import Session
from starlette.testclient import TestClient

logger = logging.getLogger(__name__)


@pytest.fixture
def mock_email(
    request: SubRequest, monkeypatch: MonkeyPatch, mocker: MockFixture
) -> Iterator[Callable]:
    monkeypatch.setenv("EMAILS_ENABLED", True)
    monkeypatch.setenv("SMTP_HOST", "ultronfakemailserver.com")
    monkeypatch.setenv("SMTP_PORT", 587)
    monkeypatch.setenv("EMAILS_FROM_EMAIL", "info@your-custom-domain.com")
    monkeypatch.setattr(settings, "EMAILS_ENABLED", True)
    monkeypatch.setattr(settings, "SMTP_HOST", "ultronfakemailserver.com")
    monkeypatch.setattr(settings, "SMTP_PORT", 587)
    monkeypatch.setattr(settings, "EMAILS_FROM_EMAIL", "info@your-custom-domain.com")

    mock_send_new_account_email = mocker.patch.object(
        users, "send_new_account_email", autospec=True
    )

    yield mock_send_new_account_email


@pytest.mark.convertingtotestclientstarlette
@pytest.mark.usersonly
@pytest.mark.unittest
class TestUserApiEndpoint:
    def test_create_user_new_email_with_starlette_client(
        self,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
        fastapi_client: TestClient,
        db: Session,
    ) -> None:
        # SOURCE: https://github.com/tiangolo/fastapi/issues/300
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)

        data = _MakeRandomNormalUserFactory()
        r = fastapi_client.post(
            f"{server_api}{settings.API_V1_STR}/users/",
            headers=superuser_token_headers,
            json=data.dict(),  # pylint: disable=no-member
        )
        assert 200 <= r.status_code < 300
        created_user = r.json()
        user = crud.user.get_by_email(db, email=data.email)
        assert user.email == created_user["email"]

    def test_get_users_superuser_me(
        self,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
        fastapi_client: TestClient,
        db: Session,
    ) -> None:
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        r = fastapi_client.get(
            f"{server_api}{settings.API_V1_STR}/users/me",
            headers=superuser_token_headers,
        )
        current_user = r.json()
        assert current_user
        assert current_user["is_active"] is True
        assert current_user["is_superuser"]
        assert current_user["email"] == settings.FIRST_SUPERUSER

    @pytest.mark.usersonly
    @pytest.mark.unittest
    def test_create_user_new_email(
        self,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
        fastapi_client: TestClient,
        db: Session,
    ) -> None:
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        # username = random_lower_string()
        # password = random_lower_string()

        data = _MakeRandomNormalUserFactory()
        # data = {"email": data.email, "password": data.password}

        r = fastapi_client.post(
            f"{server_api}{settings.API_V1_STR}/users/",
            headers=superuser_token_headers,
            json=data.dict(),  # pylint: disable=no-member
        )
        assert 200 <= r.status_code < 300
        created_user = r.json()
        user = crud.user.get_by_email(db, email=data.email)
        assert user.email == created_user["email"]

    @pytest.mark.usersonly
    @pytest.mark.unittest
    def test_create_user_new_email_with_emails_enabled(
        self,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
        monkeypatch: MonkeyPatch,
        mock_email: Callable,
        fastapi_client: TestClient,
        db: Session,
    ) -> None:
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        # username = random_lower_string()
        # password = random_lower_string()

        data = _MakeRandomNormalUserFactory()
        # data = {"email": data.email, "password": data.password}

        r = fastapi_client.post(
            f"{server_api}{settings.API_V1_STR}/users/",
            headers=superuser_token_headers,
            json=data.dict(),  # pylint: disable=no-member
        )
        assert 200 <= r.status_code < 300
        created_user = r.json()
        user = crud.user.get_by_email(db, email=data.email)
        assert user.email == created_user["email"]
        mock_email.assert_called_once_with(
            email_to=data.email, username=data.email, password=data.password
        )

    @pytest.mark.usersonly
    @pytest.mark.unittest
    def test_get_existing_user(
        self,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
        fastapi_client: TestClient,
        db: Session,
    ) -> None:
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        # username = random_lower_string()
        # password = random_lower_string()

        data = _MakeRandomNormalUserFactory()

        user_in = UserCreate(email=data.email, password=data.password)
        user = crud.user.create(db, user_in=user_in)
        user_id = user.id
        r = fastapi_client.get(
            f"{server_api}{settings.API_V1_STR}/users/{user_id}",
            headers=superuser_token_headers,
        )
        assert 200 <= r.status_code < 300
        api_user = r.json()
        user = crud.user.get_by_email(db, email=data.email)
        assert user.email == api_user["email"]

    @pytest.mark.usersonly
    @pytest.mark.unittest
    def test_create_user_existing_username(
        self,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
        fastapi_client: TestClient,
        db: Session,
    ) -> None:
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        # username = random_lower_string()
        # username = email
        # password = random_lower_string()
        data = _MakeRandomNormalUserFactory()

        user_in = UserCreate(email=data.email, password=data.password)
        user = crud.user.create(db, user_in=user_in)
        # data = {"email": username, "password": password}
        r = fastapi_client.post(
            f"{server_api}{settings.API_V1_STR}/users/",
            headers=superuser_token_headers,
            json=data.dict(),  # pylint: disable=no-member
        )
        created_user = r.json()
        assert r.status_code == 400
        assert "_id" not in created_user

    @pytest.mark.usersonly
    @pytest.mark.unittest
    def test_create_user_by_normal_user(
        self, mocker: MockFixture, fastapi_client: TestClient, db: Session
    ) -> None:
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        # username = random_lower_string()
        # password = random_lower_string()
        data = _MakeRandomNormalUserFactory()
        user_in = UserCreate(email=data.email, password=data.password)
        user = crud.user.create(db, user_in=user_in)
        user_token_headers = user_authentication_headers(
            server_api, data.email, data.password
        )
        # data = {"email": username, "password": password}
        r = fastapi_client.post(
            f"{server_api}{settings.API_V1_STR}/users/",
            headers=user_token_headers,
            json=data.dict(),  # pylint: disable=no-member
        )
        assert r.status_code == 400

    @pytest.mark.xfail(
        reason="Something is wrong with the db session we are using, it doesnt update in real time"
    )
    @pytest.mark.datainconsistent
    @pytest.mark.usersonly
    @pytest.mark.unittest
    def test_update_user_me_by_normal_user(
        self, mocker: MockFixture, fastapi_client: TestClient, db: Session
    ) -> None:
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)

        # create basic user via crud
        data = _MakeRandomNormalUserFactory()
        logger.debug("data : {}".format(data))
        user_in = UserCreate(email=data.email, password=data.password)
        logger.debug("user_in : {}".format(user_in))
        user_create_crud = crud.user.create(db, user_in=user_in)
        logger.debug("user_create_crud : {}".format(jsonable_encoder(user_create_crud)))

        # get normal user token for update request
        user_token_headers = user_authentication_headers(
            server_api, data.email, data.password
        )

        user_update = UserUpdate(
            email=data.email, password=data.password, full_name=data.full_name
        )
        logger.debug("user_update : {}".format(user_update))

        json_encoded_user_update = jsonable_encoder(user_update)

        r = fastapi_client.put(
            f"{server_api}{settings.API_V1_STR}/users/me",
            headers=user_token_headers,
            json=json_encoded_user_update,
        )

        assert 200 == r.status_code
        api_user = r.json()

        # FIXME: Ok, so the put request is working, but for some reason it is not returning an updated value for full_name from the db_session, even though it is inside the database already.
        user_by_email = crud.user.get_by_email(db, email=data.email)
        logger.debug("user_by_email : {}".format(jsonable_encoder(user_by_email)))
        assert user_by_email.full_name == api_user["full_name"]

    @pytest.mark.usersonly
    @pytest.mark.unittest
    def test_retrieve_users(
        self,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
        fastapi_client: TestClient,
        db: Session,
    ) -> None:
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        # username = random_lower_string()
        # password = random_lower_string()
        data = _MakeRandomNormalUserFactory()
        user_in = UserCreate(email=data.email, password=data.password)
        user = crud.user.create(db, user_in=user_in)
        # username2 = random_lower_string()
        # password2 = random_lower_string()
        data2 = _MakeRandomNormalUserFactory()
        user_in2 = UserCreate(email=data2.email, password=data2.password)
        user2 = crud.user.create(db, user_in=user_in2)

        r = fastapi_client.get(
            f"{server_api}{settings.API_V1_STR}/users/", headers=superuser_token_headers
        )
        all_users = r.json()

        assert len(all_users) > 1
        for user in all_users:
            assert "email" in user
