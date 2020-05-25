"""Test Global Config."""
# pylint: disable=protected-access
import logging

from typing import Iterator, Tuple

# import tempfile
# import shutil
# from pathlib import Path
# from collections import ChainMap
# import copy
# from copy import deepcopy
import pytest
from pytest_mock.plugin import MockFixture

import ultron8
from ultron8 import __version__, client
from ultron8.api import settings

# import pyconfig


logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def username_and_password_first_superuser_fixtures() -> Iterator[Tuple[str, str]]:
    yield settings.FIRST_SUPERUSER, settings.FIRST_SUPERUSER_PASSWORD


@pytest.mark.clientonly
@pytest.mark.unittest
class TestUltronAPI:
    def test_instance_ultron_api(
        self,
        mocker: MockFixture,
        username_and_password_first_superuser_fixtures: Tuple[str, str],
    ) -> None:
        username, password = username_and_password_first_superuser_fixtures

        u = client.UltronAPI()
        r = u._post_login_access_token(username, password)

        # set token
        u.jwt_token = r["access_token"]

        assert u.api_endpoint == "http://localhost:11267"
        assert u.api_url == "http://localhost:11267/v1"
        assert u.endpoints == {
            "base": "http://localhost:11267",
            "api": "http://localhost:11267/v1",
            "login": "http://localhost:11267/v1/login",
            "logs": "http://localhost:11267/v1/logs",
            "metrics": "http://localhost:11267/v1/metrics",
            "token": "http://localhost:11267/v1/token",
            "home": "http://localhost:11267/v1/",
            "alive": "http://localhost:11267/v1/alive",
            "version": "http://localhost:11267/v1/version",
            "users": "http://localhost:11267/v1/users",
            "items": "http://localhost:11267/v1/items",
        }

        r_logger = u._get_logger("asyncio")

        assert r_logger == {"name": "asyncio", "level": 10, "children": []}

    def test_instance_ultron_api_with_args(self, mocker: MockFixture) -> None:
        api_endpoint = client.get_api_endpoint()

        u = client.UltronAPI(
            api_endpoint=api_endpoint, jwt_token="dfsiohjdiohjdshoijdhiojdh546"
        )

        assert u.api_endpoint == "http://localhost:11267"
        assert u.jwt_token == "dfsiohjdiohjdshoijdhiojdh546"
        assert u._headers() == {
            "accept": "application/json",
            "Authorization": f"Bearer dfsiohjdiohjdshoijdhiojdh546",
        }

        with pytest.raises(AssertionError) as excinfo:
            u._get_version()
            assert "Failed to get Version" in str(excinfo.value)

        with pytest.raises(AssertionError) as excinfo:
            u._post_login_access_token("fakeuser", "fakepassword")
            assert "Failed to get new access token" in str(excinfo.value)

    def test_post_login_access_token(
        self,
        mocker: MockFixture,
        username_and_password_first_superuser_fixtures: Tuple[str, str],
    ) -> None:
        username, password = username_and_password_first_superuser_fixtures

        u = client.UltronAPI()
        r = u._post_login_access_token(username, password)

        assert len(r["access_token"]) > 39
        assert r["token_type"] == "bearer"

    def test_get_version(
        self,
        mocker: MockFixture,
        username_and_password_first_superuser_fixtures: Tuple[str, str],
    ) -> None:
        username, password = username_and_password_first_superuser_fixtures

        u = client.UltronAPI()
        r = u._get_version()

        cur_version = f"{__version__}"
        content = {"version": cur_version}

        assert r == content

    def test_get_alive(
        self,
        mocker: MockFixture,
        username_and_password_first_superuser_fixtures: Tuple[str, str],
    ) -> None:
        username, password = username_and_password_first_superuser_fixtures

        u = client.UltronAPI()
        r = u._get_alive()

        content = {"status": "yes"}

        assert r == content

    # def test_get_users(self, mocker, username_and_password_first_superuser_fixtures):
    #     username, password = username_and_password_first_superuser_fixtures

    #     u = client.UltronAPI()
    #     r = u._get_users()

    #     # content = {"status": "yes"}

    #     # assert r == content

    # def test_get_version_sideeffect_retry_requests_not_200(self, mocker, username_and_password_first_superuser_fixtures):
    #     username, password = username_and_password_first_superuser_fixtures

    #     mocker.patch.object(
    #         u, "_retry_requests", return_value=expected_paths, autospec=True,
    #     )

    #     u = client.UltronAPI()

    #     # In [7]: debugger.dump_magic(v)
    #     # obj._content = b'{"version":"0.0.1"}'
    #     # obj._content_consumed = True
    #     # obj._next = None
    #     # obj.apparent_encoding = ascii
    #     # obj.close = <bound method Response.close of <Response [200]>>
    #     # obj.connection = <requests.adapters.HTTPAdapter object at 0x112d676d0>
    #     # obj.content = b'{"version":"0.0.1"}'
    #     # obj.cookies = <RequestsCookieJar[]>
    #     # obj.elapsed = 0:00:00.006317
    #     # obj.encoding = None
    #     # obj.headers = {'date': 'Mon, 27 Apr 2020 23:52:46 GMT', 'server': 'uvicorn', 'content-length': '19', 'content-type': 'application/json'}
    #     # obj.history = []
    #     # obj.is_permanent_redirect = False
    #     # obj.is_redirect = False
    #     # obj.iter_content = <bound method Response.iter_content of <Response [200]>>
    #     # obj.iter_lines = <bound method Response.iter_lines of <Response [200]>>
    #     # obj.json = <bound method Response.json of <Response [200]>>
    #     # obj.links = {}
    #     # obj.next = None
    #     # obj.ok = True
    #     # obj.raise_for_status = <bound method Response.raise_for_status of <Response [200]>>
    #     # obj.raw = <urllib3.response.HTTPResponse object at 0x112d62050>
    #     # obj.reason = OK
    #     # obj.request = <PreparedRequest [GET]>
    #     # obj.status_code = 200
    #     # obj.text = {"version":"0.0.1"}
    #     # obj.url = http://localhost:11267/v1/version
    #     r = u._get_version()

    #     cur_version = f"{__version__}"
    #     content = {"version": cur_version}

    #     assert r == content
