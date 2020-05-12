"""
Global test fixtures definitions.
"""
# Taken from tedi and guid_tracker

# import asyncio
import typing
import base64
import datetime
import os
from pathlib import Path

import pytest
from starlette.testclient import TestClient

from tests.utils.utils import get_server_api
from tests.utils.utils import get_superuser_token_headers
from tests.utils.utils import superuser_credentials
from tests.utils.utils import get_superuser_jwt_request
from ultron8.api.db.u_sqlite.session import db_session, Session as SessionLocal

# from ultron8.api import settings
# from ultron8.web import app

from typing import Dict
import betamax
from betamax_matchers import json_body

from tests.utils.utils import get_server_api_with_version

from fastapi import FastAPI


import requests
from starlette.testclient import AuthType
from starlette.testclient import Cookies
from starlette.testclient import DataType
from starlette.testclient import FileType
from starlette.testclient import Params
from starlette.testclient import TestClient as PureClient
from starlette.testclient import TimeOut

from ultron8.web import get_application

here = os.path.abspath(os.path.dirname(__file__))

print("here: {}".format(here))

# fixtures_path = Path('ultron8/tests/fixtures').resolve()
fixtures_path = Path("tests/fixtures").resolve()


FAKE_TIME = datetime.datetime(2020, 12, 25, 17, 5, 55)


betamax.Betamax.register_request_matcher(json_body.JSONBodyMatcher)

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = "tests/cassettes"

    record_mode = os.environ.get("ULTRON_RECORD_MODE", "once")

    config.default_cassette_options["record_mode"] = record_mode

    r = get_superuser_jwt_request()
    tokens = r.json()
    _access_token = tokens["access_token"]

    # config.define_cassette_placeholder(
    #     "<AUTH_TOKEN>", os.environ.get("ULTRON_AUTH", "x" * 20)
    # )
    config.define_cassette_placeholder("<AUTH_TOKEN>", _access_token)

    config.default_cassette_options["match_requests_on"].append("json-body")

    config.define_cassette_placeholder(
        "<BASIC_AUTH>", base64.b64encode(b":".join(superuser_credentials)).decode()
    )


@pytest.fixture
def betamax_simple_body(request):
    """Return configuration to match cassette on uri, method and body."""
    request.cls.betamax_simple_body = {"match_requests_on": ["uri", "method", "body"]}


# @pytest.fixture
# def enterprise_url(request):
#     """Configure class with enterprise url."""
#     request.cls.enterprise_url = "https://enterprise.github3.com"


class IfNoneMatchMatcher(betamax.BaseMatcher):

    name = "if-none-match"

    def match(self, request, recorded_request):
        request_header = request.headers.get("If-None-Match")
        recorded_header = recorded_request["headers"].get("If-None-Match")
        matches = True if request_header == recorded_header else False
        return matches


betamax.Betamax.register_request_matcher(IfNoneMatchMatcher)


@pytest.fixture(scope="module")
def server_api():
    return get_server_api()


@pytest.fixture(scope="module")
def superuser_token_headers() -> Dict[str, str]:
    return get_superuser_token_headers()


# @pytest.fixture()
# def client():
#     """
#     When using the 'client' fixture in test cases, we'll get full database
#     rollbacks between test cases:
#     def test_homepage(client):
#         url = app.url_path_for('homepage')
#         response = client.get(url)
#         assert response.status_code == 200
#     """
#     client = TestClient(app)
#     with TestClient(app) as client:
#         yield client


@pytest.fixture
def patch_datetime_now(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls):
            return FAKE_TIME

    monkeypatch.setattr(datetime, "datetime", mydatetime)


# @pytest.fixture()
# def client():
#     """
#     When using the 'client' fixture in test cases, we'll get full database
#     rollbacks between test cases:
#     def test_homepage(client):
#         url = app.url_path_for('homepage')
#         response = client.get(url)
#         assert response.status_code == 200
#     """
#     client = TestClient(app)
#     with TestClient(app) as client:
#         yield client


# SOURCE: https://github.com/gvbgduh/starlette-cbge/blob/c1c7b99b07f4cf21537a12b82526b9a34ff3100b/tests/conftest.py
# @pytest.yield_fixture(scope="session")
# def event_loop() -> typing.Generator:
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()

# SOURCE: https://github.com/yourfriendlydev/fastapi-backend/blob/861e876c57a00547d15bf4b9fe794ccdc5fa3d26/tests/client.py
# class TestClientFixture(PureClient):
#     def __init__(self, prefix: str = "", *args, **kwargs):
#         super(TestClient, self).__init__(*args, **kwargs)
#         self.prefix = prefix

#     def request(
#         self,
#         method: str,
#         url: str,
#         params: Params = None,
#         data: DataType = None,
#         headers: typing.MutableMapping[str, str] = None,
#         cookies: Cookies = None,
#         files: FileType = None,
#         auth: AuthType = None,
#         timeout: TimeOut = None,
#         allow_redirects: bool = None,
#         proxies: typing.MutableMapping[str, str] = None,
#         hooks: typing.Any = None,
#         stream: bool = None,
#         verify: typing.Union[bool, str] = None,
#         cert: typing.Union[str, typing.Tuple[str, str]] = None,
#         json: typing.Any = None,
#     ) -> requests.Response:
#         url = self.prefix + url
#         return super(TestClient, self).request(
#             method,
#             url,
#             params,
#             data,
#             headers,
#             cookies,
#             files,
#             auth,
#             timeout,
#             allow_redirects,
#             proxies,
#             hooks,
#             stream,
#             verify,
#             cert,
#             json,
#         )


@pytest.fixture(scope="class")
def fastapi_app() -> typing.Generator[FastAPI, typing.Any, None]:
    # from ultron8.web import app  # pylint:disable=import-outside-toplevel
    # yield app
    _app = get_application()
    yield _app


# SOURCE: https://github.com/gvbgduh/starlette-cbge/blob/c1c7b99b07f4cf21537a12b82526b9a34ff3100b/tests/conftest.py
# @pytest.fixture(scope="session")
@pytest.fixture(scope="class")
def fastapi_client(request, fastapi_app) -> typing.Generator:
    """
    Sync test client.

    When using the 'client' fixture in test cases, we'll get full database
    rollbacks between test cases:
    def test_homepage(client):
        url = app.url_path_for('homepage')
        response = client.get(url)
        assert response.status_code == 200
    """
    # from ultron8.web import app  # pylint:disable=import-outside-toplevel

    base_url = get_server_api_with_version()

    with TestClient(app=fastapi_app, base_url=base_url) as fast_client:
        request.cls.fastapi_client = fast_client
        yield fast_client


# SOURCE: https://github.com/KyriakosFrang/sandbox/blob/c98be415c6b7e01768c4ab2d086e147cdc86757c/fastAPI_sandbox/backend/app/app/tests/conftest.py
# @pytest.fixture(scope="module")
# def superuser_token_headers(client: TestClient) -> Dict[str, str]:
#     return get_superuser_token_headers(client)


# SOURCE: https://github.com/KyriakosFrang/sandbox/blob/c98be415c6b7e01768c4ab2d086e147cdc86757c/fastAPI_sandbox/backend/app/app/tests/conftest.py
# @pytest.fixture(scope="module")
# def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
#     return authentication_token_from_email(
#         client=client, email=settings.EMAIL_TEST_USER, db=db
#     )


@pytest.fixture(scope="session")
def db() -> typing.Generator:
    yield SessionLocal()
