"""Test u8client session"""
# pylint: disable=protected-access
import logging

# import pyconfig
import pytest
import requests

import ultron8
from ultron8.api import settings
from ultron8.u8client import session

# from ultron8 import __version__
# from ultron8 import client
from tests.utils.utils import get_superuser_jwt_request

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


@pytest.fixture(scope="function")
def username_and_password_first_superuser_fixtures():
    yield settings.FIRST_SUPERUSER, settings.FIRST_SUPERUSER_PASSWORD


@pytest.mark.clientonly
@pytest.mark.unittest
class TestUltronSession:
    def build_session(self, base_url=None):
        s = session.UltronSession()
        if base_url:
            s.base_url = base_url
        return s

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

    def test_instance_session_token_auth(self, mocker):

        r = get_superuser_jwt_request()
        tokens = r.json()
        a_token = tokens["access_token"]

        s = session.TokenAuth(a_token)
        s2 = session.TokenAuth("sdifhjidhjdsofhijehiojeh")
        s3 = session.TokenAuth(a_token)

        assert s != s2
        assert s == s3

        url = "http://localhost:11267/v1/users"

        r = requests.Request("GET", url, auth=s)
        r.prepare()
        # prepped = s.prepare_request(r)

        assert isinstance(s, ultron8.u8client.session.TokenAuth)
        assert s.token == a_token

        assert str(repr(s)) == "token {}...".format(a_token[:4])

        assert s.header_format_str.format(a_token) == "Bearer {}".format(a_token)

        # resp = s.send(prepped)
        # assert resp.status_code == 200

    # def test_instance_ultron_session(self, mocker):
    #     s - self.build_session()
    #     # r = get_superuser_jwt_request()
    #     # tokens = r.json()
    #     # a_token = tokens["access_token"]

    #     # s = session.TokenAuth(a_token)
    #     # s2 = session.TokenAuth("sdifhjidhjdsofhijehiojeh")
    #     # s3 = session.TokenAuth(a_token)

    #     # assert s != s2
    #     # assert s == s3

    #     # url = "http://localhost:11267/v1/users"

    #     # r = requests.Request("GET", url, auth=s)
    #     # prepped = r.prepare()
    #     # # prepped = s.prepare_request(r)

    #     # assert isinstance(s, ultron8.u8client.session.TokenAuth)
    #     # assert s.token == a_token

    #     # assert str(repr(s)) == "token {}...".format(a_token[:4])

    #     # assert s.header_format_str.format(a_token) == "Bearer {}".format(a_token)

    #     # # resp = s.send(prepped)
    #     # # assert resp.status_code == 200

    def test_instance_ultron_session_has_default_headers(self):
        """Assert the default headers are there upon initialization"""
        s = self.build_session()
        assert "Accept" in s.headers
        assert s.headers["Accept"] == "application/json"
        assert "Accept-Charset" in s.headers
        assert s.headers["Accept-Charset"] == "utf-8"
        assert "Content-Type" in s.headers
        assert s.headers["Content-Type"] == "application/json"
        assert "User-Agent" in s.headers
        assert s.headers["User-Agent"].startswith("ultron8.client/")

    # @mock.patch.object(requests.Session, "request")
    def test_default_timeout(self, mocker):
        """Test that default timeout values are used"""
        mocker.spy(session.UltronSession, "__init__")
        mocker.spy(session.UltronSession, "__call__")
        # request_mock = mocker.patch.object(
        #     session.requests, "Session", autospec=True
        # )

        # response = mocker.Mock()
        # response.configure_mock(status_code=200, headers={})
        # request_mock.return_value = response
        s = self.build_session()
        assert s.default_connect_timeout == 4
        assert s.default_read_timeout == 10

        mocker.spy(s, "get")
        r = s.get("http://localhost:11267/v1/version")
        assert r.status_code == 200
        assert r.url == "http://localhost:11267/v1/version"
        assert r.headers["server"] == "uvicorn"
        assert r.headers["content-type"] == "application/json"
        assert r.json() == {"version": "0.0.1"}
        # pylint: disable=no-member
        assert session.UltronSession.__init__.call_count == 1
        # assert session.UltronSession.__init__.assert_called_once_with(mocker.ANY)  # pylint: disable=no-member
        assert (
            session.UltronSession.__call__.call_count == 0
        )  # pylint: disable=no-member
        assert s.get.call_count == 1  # pylint: disable=no-member
        # assert get_spy.assert_called_once_with("http://localhost:11267/v1/version")  # pylint: disable=no-member
        print(r)
        # assert r is response
        # request_mock.assert_called_once_with(
        #     "GET", "http://localhost:11267/v1/version", allow_redirects=True,
        #     timeout=(4, 10)
        # )

    # @mock.patch.object(requests.Session, "request")
    def test_custom_timeout(self, mocker):
        """Test that custom timeout values are used"""
        request_mock = mocker.patch.object(
            session.requests.Session, "request", autospec=True
        )

        response = mocker.Mock()
        response.configure_mock(status_code=200, headers={})
        request_mock.return_value = response
        s = session.UltronSession(default_connect_timeout=300, default_read_timeout=400)
        r = s.get("http://localhost:11267/v1/version")
        assert r is response
        request_mock.assert_called_once_with(
            mocker.ANY,
            "GET",
            "http://localhost:11267/v1/version",
            allow_redirects=True,
            timeout=(300, 400),
        )

    def test_build_url(self):
        """Test that UltronSessions build basic URLs"""
        s = self.build_session()
        url = s.build_url("v1", "gists", "123456", "history")
        assert url == "http://localhost:11267/v1/gists/123456/history"

    def test_build_url_caches_built_urls(self):
        """Test that building a URL caches it"""
        s = self.build_session()
        url = s.build_url("v1", "gists", "123456", "history")
        url_parts = ("http://localhost:11267", "v1", "gists", "123456", "history")
        assert url_parts in session.__url_cache__
        assert url_parts in session.__url_cache__
        assert url in session.__url_cache__.values()

    def test_build_url_uses_a_different_base(self):
        """Test that you can pass in a different base URL to build_url"""
        s = self.build_session()
        url = s.build_url(
            "v1", "gists", "123456", "history", base_url="http://localhost:1337"
        )
        assert url == "http://localhost:1337/v1/gists/123456/history"

    def test_build_url_respects_the_session_base_url(self):
        """Test that build_url uses the session's base_url"""
        s = self.build_session("https://enterprise.customer.com")
        url = s.build_url("gists")
        assert url == "https://enterprise.customer.com/gists"

    def test_basic_login_does_not_use_falsey_values(self):
        """Test that basic auth will not authenticate with falsey values"""
        bad_auths = [
            (None, "password"),
            ("username", None),
            ("", "password"),
            ("username", ""),
        ]
        for auth in bad_auths:
            # Make sure we have a clean session to test with
            s = self.build_session()
            s.basic_auth(*auth)
            assert s.auth != session.BasicAuth(*auth)

    def test_basic_login(self, username_and_password_first_superuser_fixtures):
        """Test that basic auth will work with a valid combination"""
        username, password = username_and_password_first_superuser_fixtures
        s = self.build_session()
        s.basic_auth(username, password)
        assert s.auth == session.BasicAuth(username, password)

    def test_basic_login_disables_token_auth(
        self, username_and_password_first_superuser_fixtures
    ):
        """Test that basic auth will remove the Authorization header.

        Token and basic authentication will conflict so remove the token
        authentication.
        """
        username, password = username_and_password_first_superuser_fixtures
        s = self.build_session()

        r = get_superuser_jwt_request()
        tokens = r.json()
        a_token = tokens["access_token"]

        s.token_auth(a_token)
        req = requests.Request("GET", "http://localhost:11267/v1/users")
        pr = s.prepare_request(req)
        assert "Bearer {}".format(a_token) == pr.headers["Authorization"]
        s.basic_auth(username, password)
        pr = s.prepare_request(req)
        assert "Bearer {}".format(a_token) != pr.headers["Authorization"]

    # @mock.patch.object(requests.Session, "request")
    def test_handle_two_factor_auth(self, mocker):
        """Test the method that handles getting the 2fa code"""
        request_mock = mocker.patch.object(session.requests.Session, "request")
        s = self.build_session()
        s.two_factor_auth_callback(lambda: "fake")
        args = (mocker.ANY, "GET", "http://localhost:11267/v1/users")
        s.handle_two_factor_auth(args, {})
        request_mock.assert_called_once_with(*args, headers={"X-UltronAPI-OTP": "fake"})

    # @mock.patch.object(requests.Session, "request")
    def test_request_ignores_responses_that_do_not_require_2fa(self, mocker):
        """Test that request does not try to handle 2fa when it should not"""
        request_mock = mocker.patch.object(
            session.requests.Session, "request", autospec=True
        )
        response = mocker.Mock()
        response.configure_mock(status_code=200, headers={})
        request_mock.return_value = response
        s = self.build_session()
        s.two_factor_auth_callback(lambda: "fake")
        r = s.get("http://localhost:11267/v1/users")
        assert r is response
        request_mock.assert_called_once_with(
            mocker.ANY,
            "GET",
            "http://localhost:11267/v1/users",
            allow_redirects=True,
            timeout=(4, 10),
        )

    # @mock.patch.object(requests.Session, "request")
    def test_creates_history_while_handling_2fa(self, mocker):
        """Test that the overridden request method will create history"""
        request_mock = mocker.patch.object(
            session.requests.Session, "request", autospec=True
        )
        response = mocker.Mock()
        response.configure_mock(
            status_code=401, headers={"X-UltronAPI-OTP": "required;2fa"}, history=[],
        )
        request_mock.return_value = response
        s = self.build_session()
        s.two_factor_auth_callback(lambda: "fake")
        r = s.get("http://localhost:11267/v1/users")
        assert len(r.history) != 0
        assert request_mock.call_count == 2

    def test_token_auth(self):
        """Test that token auth will work with a valid token"""
        s = self.build_session()

        r = get_superuser_jwt_request()
        tokens = r.json()
        a_token = tokens["access_token"]

        s.token_auth(a_token)

        # s.token_auth("token goes here")
        req = requests.Request("GET", "http://localhost:11267/v1/users")
        pr = s.prepare_request(req)
        assert pr.headers["Authorization"] == "Bearer {}".format(a_token)

    def test_token_auth_disables_basic_auth(
        self, username_and_password_first_superuser_fixtures
    ):
        """Test that using token auth removes the value of the auth attribute.

        If `GitHubSession.auth` is set then it conflicts with the token value.
        """
        username, password = username_and_password_first_superuser_fixtures

        s = self.build_session()

        r = get_superuser_jwt_request()
        tokens = r.json()
        a_token = tokens["access_token"]

        s.auth = (username, password)
        s.token_auth(a_token)
        assert s.auth != (username, password)
        assert isinstance(s.auth, session.TokenAuth)

    def test_token_auth_does_not_use_falsey_values(self):
        """Test that token auth will not authenticate with falsey values"""
        bad_tokens = [None, ""]
        req = requests.Request("GET", "http://localhost:11267/v1/users")
        for token in bad_tokens:
            s = self.build_session()
            s.token_auth(token)
            pr = s.prepare_request(req)
            assert "Authorization" not in pr.headers

    # def test_token_auth_with_netrc_works(self, tmpdir):
    #     """
    #     Test that token auth will be used instead of netrc.

    #     With no auth specified, requests will use any matching auths
    #     in .netrc/_netrc files
    #     """
    #     token = "my-valid-token"
    #     s = self.build_session()
    #     s.token_auth(token)

    #     netrc_contents = (
    #         "machine api.github.com\n"
    #         "login sigmavirus24\n"
    #         "password invalid_token_for_test_verification\n"
    #     )
    #     # cover testing netrc behaviour on different OSs
    #     dotnetrc = tmpdir.join(".netrc")
    #     dotnetrc.write(netrc_contents)
    #     dashnetrc = tmpdir.join("_netrc")
    #     dashnetrc.write(netrc_contents)

    #     with mock.patch.dict("os.environ", {"HOME": str(tmpdir)}):
    #         # prepare_request triggers reading of .netrc files
    #         pr = s.prepare_request(
    #             requests.Request(
    #                 "GET", "https://api.github.com/users/sigmavirus24"
    #             )
    #         )
    #         auth_header = pr.headers["Authorization"]
    #         assert auth_header == "token {0}".format(token)

    def test_two_factor_auth_callback_handles_None(self):
        s = self.build_session()
        assert s.two_factor_auth_cb is None
        s.two_factor_auth_callback(None)
        assert s.two_factor_auth_cb is None

    def test_two_factor_auth_callback_checks_for_Callable(self):
        s = self.build_session()
        assert s.two_factor_auth_cb is None
        with pytest.raises(ValueError):
            s.two_factor_auth_callback(1)

    def test_two_factor_auth_callback_accepts_a_Callable(self):
        s = self.build_session()
        assert s.two_factor_auth_cb is None
        # You have to have a sense of humor ;)

        def _not_so_anonymous(*args):
            return "foo"

        not_so_anonymous = _not_so_anonymous
        s.two_factor_auth_callback(not_so_anonymous)
        assert s.two_factor_auth_cb is not_so_anonymous

    # def test_oauth2_auth(self):
    #     """Test that oauth2 authentication works

    #     For now though, it doesn't because it isn't implemented.
    #     """
    #     s = self.build_session()
    #     with pytest.raises(NotImplementedError):
    #         s.oauth2_auth("Foo", "bar")

    def test_issubclass_of_requests_Session(self):
        """Test that GitHubSession is a subclass of requests.Session"""
        assert issubclass(session.UltronSession, requests.Session)

    def test_can_use_temporary_basic_auth(
        self, username_and_password_first_superuser_fixtures
    ):
        """Test that temporary_basic_auth resets old auth."""
        username, password = username_and_password_first_superuser_fixtures
        s = self.build_session()
        s.basic_auth(username, password)
        with s.temporary_basic_auth("temp", "pass"):
            assert s.auth != session.BasicAuth(username, password)

        assert s.auth == session.BasicAuth(username, password)

    def test_temporary_basic_auth_replaces_auth(
        self, username_and_password_first_superuser_fixtures
    ):
        """Test that temporary_basic_auth sets the proper credentials."""
        username, password = username_and_password_first_superuser_fixtures
        s = self.build_session()
        # s.basic_auth("foo", "bar")
        s.basic_auth(username, password)
        with s.temporary_basic_auth("temp", "pass"):
            assert s.auth == session.BasicAuth("temp", "pass")

    def test_no_auth(self, username_and_password_first_superuser_fixtures):
        """Verify that no_auth removes existing authentication."""
        username, password = username_and_password_first_superuser_fixtures
        s = self.build_session()
        s.basic_auth("user", "password")
        req = requests.Request("GET", "http://localhost:11267/v1/users")

        with s.no_auth():
            pr = s.prepare_request(req)
            assert "Authorization" not in pr.headers
            assert s.auth is None

        pr = s.prepare_request(req)
        assert "Authorization" in pr.headers
        assert s.auth == session.BasicAuth("user", "password")

    def test_retrieve_client_credentials_when_set(self):
        """Test that retrieve_client_credentials will return the credentials.

        We must assert that when set, this function will return them.
        """
        s = self.build_session()
        s.params = {"client_id": "id", "client_secret": "secret"}
        assert s.retrieve_client_credentials() == ("id", "secret")

    def test_retrieve_client_credentials_returns_none(self):
        """Test that retrieve_client_credentials will return (None, None).

        Namely, then the necessary parameters are set, it will not raise an
        error.
        """
        s = self.build_session()
        assert s.retrieve_client_credentials() == (None, None)

    def test_pickling(self):
        s = self.build_session("http://localhost:11267/v1/users")
        dumped = pickle.dumps(s, pickle.HIGHEST_PROTOCOL)
        loaded = pickle.loads(dumped)

        assert hasattr(loaded, "base_url")
        assert hasattr(loaded, "two_factor_auth_cb")

        assert loaded.base_url == s.base_url
        assert loaded.two_factor_auth_cb == s.two_factor_auth_cb
