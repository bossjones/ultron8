"""Test u8client models"""
# pylint: disable=protected-access
from copy import copy
from datetime import datetime, timedelta
import io
import json
import logging
import os

import pytest
import requests

import ultron8
from ultron8.api import settings
from ultron8.exceptions.client import (
    UltronClientError,
    UnexpectedResponse,
    UnprocessableResponseBody,
)
from ultron8.u8client import session
from ultron8.u8client.models import UltronCore

from tests.utils.user import user_authentication_headers
from tests.utils.utils import (
    get_server_api,
    get_superuser_jwt_request,
    random_email,
    random_lower_string,
)

try:
    import cPickle as pickle
except ImportError:
    import pickle


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


class MyTestRefreshClass(UltronCore):
    """Subclass for testing refresh on UltronCore."""

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
def example_data(request, server_api):
    last_modified = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    url = f"{server_api}{settings.API_V1_STR}/users/"
    etag = "644b5b0155e6404a9cc4bd9d8b1ae730"
    example_data = {
        "url": url,
        "last_modified": last_modified,
        "etag": etag,
        "fake_attr": "users",
    }

    yield example_data


@pytest.fixture
def get_user_class_representation(request, example_data):
    # last_modified = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    # url = f"{server_api}{settings.API_V1_STR}/users/"
    # etag = "644b5b0155e6404a9cc4bd9d8b1ae730"
    # example_data = {
    #     "url": url,
    #     "last_modified": last_modified,
    #     "etag": etag,
    #     "fake_attr": "users",
    # }

    s = build_session()
    user_class = MyTestRefreshClass(example_data, s)
    request.cls.mytestrefreshclass = user_class
    request.cls.example_data = example_data

    yield user_class


def build_url(self, *args, **kwargs):
    """A function to proxy to the actual GitHubSession#build_url method."""
    # We want to assert what is happening with the actual calls to the
    # Internet. We can proxy this.
    return ultron8.u8client.session.UltronSession().build_url(*args, **kwargs)


@pytest.mark.clientonly
@pytest.mark.unittest
class TestUltronCore:
    @staticmethod
    def get_build_url_proxy():
        return build_url

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

    def test_exposes_attributes(self, get_user_class_representation):
        """Verify JSON attributes are exposed even if not explicitly set."""
        assert get_user_class_representation.fake_attr == "users"

    def test_from_json(self, get_user_class_representation):
        """Verify that method returns GitHubObject from json."""
        s = build_session()
        ultron_core = UltronCore.from_json("{}", s)
        assert isinstance(ultron_core, UltronCore)

    def test_instance_or_null(self, get_user_class_representation):
        """Verify method raises exception when json is not a dict."""
        with pytest.raises(UnprocessableResponseBody):
            get_user_class_representation._instance_or_null(UltronCore, [])

    def test_json(self, get_user_class_representation):
        """Verify JSON information is retrieved correctly."""
        response = requests.Response()
        response.headers["Last-Modified"] = "foo"
        response.headers["ETag"] = "bar"
        response.raw = io.BytesIO(b"{}")
        response.status_code = 200

        json = get_user_class_representation._json(response, 200)
        assert json["Last-Modified"] == "foo"
        assert json["ETag"] == "bar"

    def test_json_status_code_does_not_match(self, get_user_class_representation):
        """Verify JSON information is retrieved correctly."""
        response = requests.Response()
        response.status_code = 204

        with pytest.raises(UnexpectedResponse):
            get_user_class_representation._json(response, 200)

    def test_missingattribute(self, get_user_class_representation):
        """Test AttributeError is raised when attribute is not in JSON."""
        with pytest.raises(AttributeError):
            get_user_class_representation.missingattribute

    def test_refresh(self, request, example_data, mocker, monkeypatch):
        """Verify the request of refreshing an object."""

        # Create a mocket session and pre populate it with values
        MockedSession = mocker.create_autospec(session.UltronSession)
        _session = MockedSession()
        base_attrs = ["headers", "auth"]
        args = []
        attrs = dict((key, mocker.Mock()) for key in set(args).union(base_attrs))
        _session.configure_mock(**attrs)
        _session.delete.return_value = None
        _session.get.return_value = None
        _session.patch.return_value = None
        _session.post.return_value = None
        _session.put.return_value = None
        _session.has_auth.return_value = True
        _session.build_url = self.get_build_url_proxy()

        # Monkeypatch function to proxy to the actual UltronSession#build_url method
        monkeypatch.setattr(
            MyTestRefreshClass, "_build_url", self.get_build_url_proxy()
        )

        # Create Test Subclass
        user_class = MyTestRefreshClass(example_data, _session)

        # Override the _build_url function to the proxy function
        user_class._build_url = self.get_build_url_proxy()

        # refresh data
        instance = user_class.refresh()

        # verify the instance we get back is infact a subclass of MyTestRefreshClass
        assert isinstance(instance, MyTestRefreshClass)

        expected_headers = None
        _session.get.assert_called_once_with(
            example_data["url"], headers=expected_headers
        )

    def test_refresh_custom_headers(self, request, example_data, mocker, monkeypatch):
        """Verify the request of refreshing an object."""

        # Create a mocket session and pre populate it with values
        MockedSession = mocker.create_autospec(session.UltronSession)
        _session = MockedSession()
        base_attrs = ["headers", "auth"]
        args = []
        attrs = dict((key, mocker.Mock()) for key in set(args).union(base_attrs))
        _session.configure_mock(**attrs)
        _session.delete.return_value = None
        _session.get.return_value = None
        _session.patch.return_value = None
        _session.post.return_value = None
        _session.put.return_value = None
        _session.has_auth.return_value = True
        _session.build_url = self.get_build_url_proxy()

        # Monkeypatch function to proxy to the actual UltronSession#build_url method
        monkeypatch.setattr(
            MyTestRefreshClass, "_build_url", self.get_build_url_proxy()
        )

        # Create Test Subclass
        user_class = MyTestRefreshClass(example_data, _session)

        # Override the _build_url function to the proxy function
        user_class._build_url = self.get_build_url_proxy()

        user_class.CUSTOM_HEADERS = {
            "Accept": "application/vnd.github.drax-preview+json"
        }
        expected_headers = {"Accept": "application/vnd.github.drax-preview+json"}

        user_class.refresh()

        _session.get.assert_called_once_with(
            example_data["url"], headers=expected_headers
        )

    def test_refresh_last_modified(self, request, example_data, mocker, monkeypatch):
        """Verify the request of refreshing an object."""

        # Create a mocket session and pre populate it with values
        MockedSession = mocker.create_autospec(session.UltronSession)
        _session = MockedSession()
        base_attrs = ["headers", "auth"]
        args = []
        attrs = dict((key, mocker.Mock()) for key in set(args).union(base_attrs))
        _session.configure_mock(**attrs)
        _session.delete.return_value = None
        _session.get.return_value = None
        _session.patch.return_value = None
        _session.post.return_value = None
        _session.put.return_value = None
        _session.has_auth.return_value = True
        _session.build_url = self.get_build_url_proxy()

        # Monkeypatch function to proxy to the actual UltronSession#build_url method
        monkeypatch.setattr(
            MyTestRefreshClass, "_build_url", self.get_build_url_proxy()
        )

        # Create Test Subclass
        user_class = MyTestRefreshClass(example_data, _session)

        # Override the _build_url function to the proxy function
        user_class._build_url = self.get_build_url_proxy()

        expected_headers = {"If-Modified-Since": example_data["last_modified"]}

        user_class.refresh(conditional=True)

        _session.get.assert_called_once_with(
            example_data["url"], headers=expected_headers
        )

    def test_refresh_etag(self, request, example_data, mocker, monkeypatch):
        """Verify the request of refreshing an object."""

        # Create a mocket session and pre populate it with values
        MockedSession = mocker.create_autospec(session.UltronSession)
        _session = MockedSession()
        base_attrs = ["headers", "auth"]
        args = []
        attrs = dict((key, mocker.Mock()) for key in set(args).union(base_attrs))
        _session.configure_mock(**attrs)
        _session.delete.return_value = None
        _session.get.return_value = None
        _session.patch.return_value = None
        _session.post.return_value = None
        _session.put.return_value = None
        _session.has_auth.return_value = True
        _session.build_url = self.get_build_url_proxy()

        # Monkeypatch function to proxy to the actual UltronSession#build_url method
        monkeypatch.setattr(
            MyTestRefreshClass, "_build_url", self.get_build_url_proxy()
        )

        # Create Test Subclass
        user_class = MyTestRefreshClass(example_data, _session)

        # Override the _build_url function to the proxy function
        user_class._build_url = self.get_build_url_proxy()

        user_class.last_modified = None

        expected_headers = {"If-None-Match": example_data["etag"]}

        user_class.refresh(conditional=True)

        _session.get.assert_called_once_with(
            example_data["url"], headers=expected_headers
        )

    def test_refresh_json(self, request, example_data, mocker, monkeypatch):
        """Verify refreshing an object updates stored json data."""

        # Create a mocket session and pre populate it with values
        MockedSession = mocker.create_autospec(session.UltronSession)
        _session = MockedSession()
        base_attrs = ["headers", "auth"]
        args = []
        attrs = dict((key, mocker.Mock()) for key in set(args).union(base_attrs))
        _session.configure_mock(**attrs)
        _session.delete.return_value = None
        _session.get.return_value = None
        _session.patch.return_value = None
        _session.post.return_value = None
        _session.put.return_value = None
        _session.has_auth.return_value = True
        _session.build_url = self.get_build_url_proxy()

        # Monkeypatch function to proxy to the actual UltronSession#build_url method
        monkeypatch.setattr(
            MyTestRefreshClass, "_build_url", self.get_build_url_proxy()
        )

        # Create Test Subclass
        user_class = MyTestRefreshClass(example_data, _session)

        # Override the _build_url function to the proxy function
        user_class._build_url = self.get_build_url_proxy()

        expected_data = {"changed_files": 4}
        response = requests.Response()
        response.status_code = 200
        response.raw = io.BytesIO(json.dumps(expected_data).encode("utf8"))
        _session.get.return_value = response

        user_class.refresh()

        assert "changed_files" in user_class.as_dict()
        assert user_class.changed_files == 4

    def test_strptime(self, request, example_data, mocker, monkeypatch):
        """Verify that method converts ISO 8601 formatted string."""

        # Create a mocket session and pre populate it with values
        MockedSession = mocker.create_autospec(session.UltronSession)
        _session = MockedSession()
        base_attrs = ["headers", "auth"]
        args = []
        attrs = dict((key, mocker.Mock()) for key in set(args).union(base_attrs))
        _session.configure_mock(**attrs)
        _session.delete.return_value = None
        _session.get.return_value = None
        _session.patch.return_value = None
        _session.post.return_value = None
        _session.put.return_value = None
        _session.has_auth.return_value = True
        _session.build_url = self.get_build_url_proxy()

        # Monkeypatch function to proxy to the actual UltronSession#build_url method
        monkeypatch.setattr(
            MyTestRefreshClass, "_build_url", self.get_build_url_proxy()
        )

        # Create Test Subclass
        user_class = MyTestRefreshClass(example_data, _session)

        # Override the _build_url function to the proxy function
        user_class._build_url = self.get_build_url_proxy()

        dt = user_class._strptime("2015-06-18T19:53:04Z")
        assert dt.tzname() == "UTC"
        assert dt.dst() == timedelta(0)
        assert dt.utcoffset() == timedelta(0)

    def test_strptime_time_str_required(
        self, request, example_data, mocker, monkeypatch
    ):
        """Verify that method converts ISO 8601 formatted string."""

        # Create a mocket session and pre populate it with values
        MockedSession = mocker.create_autospec(session.UltronSession)
        _session = MockedSession()
        base_attrs = ["headers", "auth"]
        args = []
        attrs = dict((key, mocker.Mock()) for key in set(args).union(base_attrs))
        _session.configure_mock(**attrs)
        _session.delete.return_value = None
        _session.get.return_value = None
        _session.patch.return_value = None
        _session.post.return_value = None
        _session.put.return_value = None
        _session.has_auth.return_value = True
        _session.build_url = self.get_build_url_proxy()

        # Monkeypatch function to proxy to the actual UltronSession#build_url method
        monkeypatch.setattr(
            MyTestRefreshClass, "_build_url", self.get_build_url_proxy()
        )

        # Create Test Subclass
        user_class = MyTestRefreshClass(example_data, _session)

        # Override the _build_url function to the proxy function
        user_class._build_url = self.get_build_url_proxy()

        assert user_class._strptime("") is None

    def test_can_be_copied(self, request, example_data, mocker, monkeypatch):
        """Verify that a UltronCore object can be copied."""

        # Create a mocket session and pre populate it with values
        MockedSession = mocker.create_autospec(session.UltronSession)
        _session = MockedSession()
        base_attrs = ["headers", "auth"]
        args = []
        attrs = dict((key, mocker.Mock()) for key in set(args).union(base_attrs))
        _session.configure_mock(**attrs)
        _session.delete.return_value = None
        _session.get.return_value = None
        _session.patch.return_value = None
        _session.post.return_value = None
        _session.put.return_value = None
        _session.has_auth.return_value = True
        _session.build_url = self.get_build_url_proxy()

        # Monkeypatch function to proxy to the actual UltronSession#build_url method
        monkeypatch.setattr(
            MyTestRefreshClass, "_build_url", self.get_build_url_proxy()
        )

        # Create Test Subclass
        user_class = MyTestRefreshClass(example_data, _session)

        # Override the _build_url function to the proxy function
        user_class._build_url = self.get_build_url_proxy()

        assert copy(user_class) is not None
