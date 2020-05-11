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
from tests.utils.utils import get_sueruser_jwt_request


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
        assert str(repr(s)) == "basic {}".format(username)

    def test_instance_session_token(self, mocker):

        r = get_sueruser_jwt_request()
        tokens = r.json()
        a_token = tokens["access_token"]

        s = session.TokenAuth(a_token)
        s2 = session.TokenAuth("sdifhjidhjdsofhijehiojeh")
        s3 = session.TokenAuth(a_token)

        assert s != s2
        assert s == s3

        url = "http://localhost:11267/v1/users"

        r = requests.Request("GET", url, auth=s)
        prepped = r.prepare()
        # prepped = s.prepare_request(r)

        assert isinstance(s, ultron8.u8client.session.TokenAuth)
        assert s.token == a_token

        assert str(repr(s)) == "token {}...".format(a_token[:4])

        assert s.header_format_str.format(a_token) == "Bearer {}".format(a_token)

        # resp = s.send(prepped)
        # assert resp.status_code == 200
