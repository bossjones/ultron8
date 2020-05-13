"""Test u8client models"""
# pylint: disable=protected-access
import logging
import io
import os
from copy import copy
from datetime import datetime, timedelta

try:
    import cPickle as pickle
except ImportError:
    import pickle

import pytest

import requests

import ultron8
from ultron8.u8client.models import UltronCore

from ultron8.api import settings
from tests.utils.utils import get_superuser_jwt_request

from tests.utils.user import user_authentication_headers
from tests.utils.utils import get_server_api
from tests.utils.utils import random_lower_string, random_email
from ultron8.u8client import session

from ultron8.exceptions.client import UltronClientError

logger = logging.getLogger(__name__)

#####################################################################
# SOURCE: https://github.com/saurabhsharma92/Face-recognition/blob/0613110f44722b74808091ad8160fb61285b30d7/venv/Lib/site-packages/tests/test_api_client.py
#####################################################################
def empty_response(*args, **kwargs):
    resp = requests.Response()
    resp._content = b"{}"
    resp.status_code = 200
    return resp


def empty_json(*args, **kwargs):
    return {}


@pytest.fixture
def auth():
    return "1234567890"


@pytest.fixture
def auth_header(auth):
    return {"Authorization": "Token %s" % auth, "Accept": "application/json"}


#####################################################################
# SOURCE: https://github.com/saurabhsharma92/Face-recognition/blob/0613110f44722b74808091ad8160fb61285b30d7/venv/Lib/site-packages/tests/test_api_client.py <END
#####################################################################


# @pytest.fixture(scope="function")
# def username_and_password_first_superuser_fixtures():
#     yield settings.FIRST_SUPERUSER, settings.FIRST_SUPERUSER_PASSWORD


class MyTestRefreshClass(UltronCore):
    """Subclass for testing refresh on GitHubCore."""

    def __init__(self, example_data, session):
        super(MyTestRefreshClass, self).__init__(example_data, session)
        self._api = example_data["url"]
        self.last_modified = example_data["last_modified"]
        self.etag = example_data["etag"]


def build_session(base_url=None):
    s = session.UltronSession()
    if base_url:
        s.base_url = base_url
    return s


@pytest.fixture
def get_user_class_representation(request, server_api):
    last_modified = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    url = f"{server_api}{settings.API_V1_STR}/users/"
    etag = "644b5b0155e6404a9cc4bd9d8b1ae730"
    example_data = {
        "url": url,
        "last_modified": last_modified,
        "etag": etag,
        "fake_attr": "users",
    }

    s = build_session()
    user_class = MyTestRefreshClass(example_data, s)

    yield user_class


@pytest.mark.clientonly
@pytest.mark.unittest
class TestUltronCore:
    def test_boolean(self, get_user_class_representation):
        """Verify boolean tests for response codes correctly."""
        response = requests.Response()
        response.status_code = 200
        boolean = get_user_class_representation._boolean(
            response=response, true_code=200, false_code=204
        )

        assert boolean is True

    def test_boolean_raises_exception(self, get_user_class_representation):
        """Verify boolean tests for response codes correctly."""
        response = requests.Response()
        response.status_code = 512
        response.raw = io.BytesIO()
        with pytest.raises(UltronClientError):
            get_user_class_representation._boolean(
                response=response, true_code=200, false_code=204
            )

    def test_boolean_false_code(self, get_user_class_representation):
        """Verify boolean tests for response codes correctly."""
        response = requests.Response()
        response.status_code = 204
        boolean = get_user_class_representation._boolean(
            response=response, true_code=200, false_code=204
        )

        assert boolean is False

    def test_boolean_empty_response(self, get_user_class_representation):
        """Verify boolean tests for response codes correctly."""
        boolean = get_user_class_representation._boolean(
            response=None, true_code=200, false_code=204
        )

        assert boolean is False

    # def test_my_test_refresh_class(self, get_user_class_representation):
    #     # NOTE: We want to be using fastapi_client here, and maybe even session, db fixtures.
    #     pass
