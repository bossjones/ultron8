"""Test u8client session"""
# pylint: disable=protected-access
import logging
import os

import pytest

# import pyconfig
import requests

import ultron8
from ultron8.u8client import session

# from ultron8 import __version__
# from ultron8 import client
from ultron8.api import settings


logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def username_and_password_first_superuser_fixtures():
    yield settings.FIRST_SUPERUSER, settings.FIRST_SUPERUSER_PASSWORD


@pytest.mark.clientonly
@pytest.mark.unittest
class TestUltronAPI:
    def test_instance_session_basic_auth(
        self, mocker, username_and_password_first_superuser_fixtures
    ):
        username, password = username_and_password_first_superuser_fixtures

        s = session.BasicAuth(username, password)

        # # Now prove it works
        # r = s.get("http://localhost:11267/v1/users")

        url = "http://localhost:11267/v1/users"

        r = requests.Request("GET", url, auth=s)
        p = r.prepare()

        assert isinstance(s, ultron8.u8client.session.BasicAuth)
        assert s.password == "password"
        assert s.username == "admin@ultron8.com"

        assert p.headers["Authorization"] == requests.auth._basic_auth_str(
            username, password
        )
        assert "Basic " in p.headers["Authorization"]
