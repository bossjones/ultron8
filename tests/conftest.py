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
from contextlib import contextmanager

import tempfile
import logging
import platform
import posixpath
import os
import shutil
from pathlib import Path
from collections import ChainMap
import copy
from copy import deepcopy

import pytest
from starlette.testclient import TestClient

from tests.utils.utils import get_server_api
from tests.utils.utils import get_superuser_token_headers
from tests.utils.utils import superuser_credentials
from tests.utils.utils import get_superuser_jwt_request

from ultron8.api.db.u_sqlite.session import SessionLocal

# from ultron8.api import settings
# from ultron8.web import app

from typing import Any, Generator, Iterator, Tuple, Dict
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
from ultron8.api import settings

from tests.utils.user import authentication_token_from_email
from _pytest.fixtures import SubRequest
from _pytest.monkeypatch import MonkeyPatch
from fastapi.applications import FastAPI

# from tests.utils.user import get_superuser_token_headers

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
def server_api() -> str:
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


@pytest.fixture(scope="function")
def fastapi_app() -> typing.Generator[FastAPI, typing.Any, None]:
    # from ultron8.web import app  # pylint:disable=import-outside-toplevel
    # yield app
    _app = get_application()
    yield _app


# SOURCE: https://github.com/gvbgduh/starlette-cbge/blob/c1c7b99b07f4cf21537a12b82526b9a34ff3100b/tests/conftest.py
# @pytest.fixture(scope="session")
@pytest.fixture(scope="function")
def fastapi_client(request: SubRequest, fastapi_app: FastAPI) -> typing.Generator:
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
# def superuser_token_headers(fastapi_client: TestClient) -> Dict[str, str]:
#     return get_superuser_token_headers()


# SOURCE: https://github.com/KyriakosFrang/sandbox/blob/c98be415c6b7e01768c4ab2d086e147cdc86757c/fastAPI_sandbox/backend/app/app/tests/conftest.py
# @pytest.fixture(scope="module")
def normal_user_token_headers(
    fastapi_client: TestClient, db: SessionLocal
) -> Dict[str, str]:
    return authentication_token_from_email(
        client=fastapi_client, email=settings.EMAIL_TEST_USER, db=db
    )


# @pytest.fixture(scope="session")
@pytest.fixture(scope="function")
def db() -> typing.Generator:
    yield SessionLocal()


# SOURCE: https://github.com/gvbgduh/starlette-cbge/blob/c1c7b99b07f4cf21537a12b82526b9a34ff3100b/tests/conftest.py
# @pytest.mark.asyncio
# @pytest.fixture(scope="session")
# async def async_client() -> typing.AsyncGenerator:
#     """
#     Async test client
#     """
#     from example_app.app import app

#     async with AsyncTestClient(app=app) as async_client:
#         yield async_client


# @pytest.fixture(scope="session", autouse=True)
# async def create_db_tables() -> typing.AsyncGenerator:
#     """
#     Creates tables using the helper func from the example app.
#     Also drops them when tests are complete.
#     """
#     from example_app.db import create_tables, drop_tables

#     await create_tables()
#     yield
#     await drop_tables()


# @pytest.fixture(scope="function", autouse=True)
# async def truncate_tables() -> typing.AsyncGenerator:
#     """
#     Truncates tables before every test,
#     basically to allow transactional operations complete.
#     """
#     from example_app.db import truncate_tables

#     await truncate_tables()
#     yield


@pytest.fixture(scope="function")
def first_superuser_username_and_password_fixtures() -> Iterator[Tuple[str, str]]:
    yield settings.FIRST_SUPERUSER, settings.FIRST_SUPERUSER_PASSWORD


#####################################################
# SOURCE: https://github.com/thorwolpert/lear-gh/blob/596930fd2a6b77ab303c73db53d608c89de97110/queue_services/common/tests/conftest.py
#####################################################
EPOCH_DATETIME = datetime.datetime.utcfromtimestamp(0)
FROZEN_DATETIME = datetime.datetime(2001, 8, 5, 7, 7, 58, 272362)


def add_years(d, years):
    """Return a date that's `years` years after the date (or datetime).
    Return the same calendar date (month and day) in the destination year,
    if it exists, otherwise use the following day
    (thus changing February 29 to February 28).
    """
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return d + (datetime.date(d.year + years, 3, 1) - datetime.date(d.year, 3, 1))


# fixture to freeze utcnow to a fixed date-time
@pytest.fixture
def freeze_datetime_utcnow(monkeypatch):
    """Fixture to return a static time for utcnow()."""

    class _Datetime:
        @classmethod
        def utcnow(cls):
            return FROZEN_DATETIME

    monkeypatch.setattr(datetime, "datetime", _Datetime)


@contextmanager
def not_raises(exception):
    """Corallary to the pytest raises builtin.
    Assures that an exception is NOT thrown.
    """
    try:
        yield
    except exception:
        raise pytest.fail(f"DID RAISE {exception}")


#####################################################
# SOURCE: https://github.com/thorwolpert/lear-gh/blob/596930fd2a6b77ab303c73db53d608c89de97110/queue_services/common/tests/conftest.py
#####################################################


@pytest.fixture
def create_mocked_ultron_session(request, mocker):
    """Use mock to auto-spec a UltronSession and return an instance."""
    from ultron8.u8client import session

    MockedSession = mocker.create_autospec(session.UltronSession)
    # request.cls.fastapi_client = fast_client
    yield MockedSession()


# @pytest.fixture
# def create_session_mock(mocker, *args):
#     """Create a mocked session and add headers and auth attributes."""
#     session = self.create_mocked_session()
#     base_attrs = ["headers", "auth"]
#     attrs = dict(
#         (key, mock.Mock()) for key in set(args).union(base_attrs)
#     )
#     session.configure_mock(**attrs)
#     session.delete.return_value = None
#     session.get.return_value = None
#     session.patch.return_value = None
#     session.post.return_value = None
#     session.put.return_value = None
#     session.has_auth.return_value = True
#     session.build_url = self.get_build_url_proxy()
#     return session


##############################################################################
# Boilerplate for isolated systems
##############################################################################

# https://docs.pytest.org/en/latest/tmpdir.html
@pytest.fixture(name="linux_systems_fixture")
def linux_systems_fixture(request: SubRequest, monkeypatch: MonkeyPatch) -> None:
    request.cls.systems = {
        "Linux": [{"HOME": "/home/test", "XDG_CONFIG_HOME": "~/.config"}, posixpath],
    }

    request.cls.sys_name = "Linux"

    env_override, _ = request.cls.systems["Linux"]

    for k, v in env_override.items():
        monkeypatch.setenv(k, v)

    # this is suppose to use a conditional
    # NOTE: THIS IS WHAT WE NORMALLY DO # base = tempfile.mkdtemp()
    # NOTE: THIS IS WHAT WE NORMALLY DO # fake_dir_root = tempfile.mkdtemp(prefix="config", dir=base)
    # NOTE: THIS IS WHAT WE NORMALLY DO # fake_dir = os.path.join(
    # NOTE: THIS IS WHAT WE NORMALLY DO #     fake_dir_root, "ultron8"
    # NOTE: THIS IS WHAT WE NORMALLY DO # )  # eg. /home/developer/.config/ultron8
    # NOTE: THIS IS WHAT WE NORMALLY DO # full_file_name = "smart.yaml"
    # NOTE: THIS IS WHAT WE NORMALLY DO # path = os.path.join(fake_dir, full_file_name)

    tmp = tempfile.mkdtemp(prefix="ultron8-test-")
    print(f"[linux_systems_fixture] created temp directory: {tmp}")

    tmp_xdg_config_home = os.path.join(tmp, ".config")
    tmp_ultron_config_dir = os.path.join(tmp_xdg_config_home, "ultron8")
    tmp_ultron_config_path = os.path.join(tmp_ultron_config_dir, "smart.yaml")

    os.makedirs(tmp_xdg_config_home)
    os.makedirs(tmp_ultron_config_dir)

    request.cls.home = tmp
    request.cls.xdg_config_home = tmp_xdg_config_home
    request.cls.ultron_config_dir = tmp_ultron_config_dir
    request.cls.ultron_config_path = tmp_ultron_config_path

    monkeypatch.setenv("HOME", request.cls.home)
    monkeypatch.setenv("XDG_CONFIG_HOME", request.cls.xdg_config_home)
    monkeypatch.setenv("ULTRON8DIR", request.cls.ultron_config_dir)

    @request.addfinalizer
    def restore():
        print(
            "starting finalizer restore after finished with fixture 'linux_systems_fixture'"
        )
        shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture(name="posixpath_fixture")
def posixpath_fixture(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(os, "path", posixpath)


@pytest.fixture(name="platform_system_fixture")
def platform_system_fixture(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(os, "system", lambda: "Linux")


@pytest.fixture(name="fixture_config_data_with_foo")
def fixture_config_data_with_foo():
    example_data = """
---
clusters_path: clusters/
cache_path: cache/
workspace_path: workspace/
templates_path: templates/

ultrons:
  - debugultron

async: True

nodes: 0

db_uri: sqlite:///test.db

flags:
    debug: 1
    verbose: 1
    keep: 1
    stderr: 1
    repeat: 0

clusters:
    instances:
        local:
            url: 'http://localhost:11267'
            token: 'memememememememmemememe'
"""
    yield example_data


@pytest.fixture(name="mock_expand_user")
def mock_expand_user(request: SubRequest, monkeypatch: MonkeyPatch) -> None:
    def mockreturn(path):
        return request.cls.home

    monkeypatch.setattr(os.path, "expanduser", mockreturn)
