import collections.abc as abc_collections
from contextlib import contextmanager
import datetime
import logging
from unittest.mock import _ANY, MagicMock, Mock

from typing import Callable, Dict, Iterator, Optional, Tuple, Union

import dateutil.parser
import requests
from requests.adapters import HTTPAdapter
from requests.models import PreparedRequest, Response
from requests.packages.urllib3.util.retry import Retry  # pylint: disable=import-error

from ultron8 import __version__
from ultron8.api import settings
from ultron8.u8client.utils import get_api_endpoint

from ultron8.exceptions.client import (  # AuthenticationFailed,; BadRequest,; CardHasNoContentUrl,; ClientError,; Conflict,; ConnectionError,; ForbiddenError,; GeneratedTokenExpired,; IncompleteResponse,; MethodNotAllowed,; MissingAppAuthentication,; MissingAppBearerAuthentication,; MissingAppInstallationAuthentication,; NotAcceptable,; NotFoundError,; NotRefreshable,; ResponseError,; ServerError,; TransportError,; UltronClientError,; UltronClientException,; UnavailableForLegalReasons,; UnexpectedResponse,; UnprocessableEntity,; UnprocessableResponseBody,
    AppInstallationTokenExpired,
    AppTokenExpired,
)

__url_cache__ = {}
logger = logging.getLogger(__name__)


def requires_2fa(response: Union[Mock, Response]) -> bool:
    """Determine whether a response requires us to prompt the user for 2FA."""
    if (
        response.status_code == 401
        and "X-UltronAPI-OTP" in response.headers
        and "required" in response.headers["X-UltronAPI-OTP"]
    ):
        return True
    return False


# NOTE: github3.py
class BasicAuth(requests.auth.HTTPBasicAuth):
    """Sub-class requests's class so we have a nice repr."""

    def __repr__(self) -> str:
        """Use the username as the representation."""
        return "basic {}".format(self.username)


# NOTE: github3.py
class TokenAuth(requests.auth.AuthBase):
    """Auth class that handles simple tokens."""

    header_format_str = "Bearer {}"

    def __init__(self, token: str) -> None:
        """Store our token."""
        self.token = token

    def __repr__(self) -> str:
        """Return a nice view of the token in use."""
        return "token {}...".format(self.token[:4])

    # https://mypy.readthedocs.io/en/stable/dynamic_typing.html
    def __ne__(self, other: Union[Tuple[str, str], "TokenAuth"]) -> bool:
        """Test for equality, or the lack thereof."""
        return not self == other

    # https://mypy.readthedocs.io/en/stable/dynamic_typing.html
    def __eq__(self, other: Union[Tuple[str, str], "TokenAuth"]) -> bool:
        """Test for equality, or the lack thereof."""
        return self.token == getattr(other, "token", None)

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        """Add the authorization header and format it."""
        request.headers["Authorization"] = self.header_format_str.format(self.token)
        return request


class UltronSession(requests.Session):
    """Our slightly specialized Session object.

    Normally this is created automatically by
    :class:`~ultron8.api.UltronAPI`.  To use alternate values for
    network timeouts, this class can be instantiated directly and
    passed to the UltronAPI object.  For example:

    .. code-block:: python

       gh = ultron8.api.UltronAPI(session=session.UltronSession(
           default_connect_timeout=T, default_read_timeout=N))

    :param default_connect_timeout:
       the number of seconds to wait when establishing a connection to
       UltronAPI
    :type default_connect_timeout:
       float
    :param default_read_timeout:
       the number of seconds to wait for a response from UltronAPI
    :type default_read_timeout:
       float
    """

    auth = None
    __attrs__ = requests.Session.__attrs__ + [
        "base_url",
        "two_factor_auth_cb",
        "default_connect_timeout",
        "default_read_timeout",
        "request_counter",
    ]

    def __init__(
        self, default_connect_timeout: int = 4, default_read_timeout: int = 10
    ) -> None:
        """Slightly modify how we initialize our session."""
        super(UltronSession, self).__init__()
        self.default_connect_timeout = default_connect_timeout
        self.default_read_timeout = default_read_timeout
        self.headers.update(
            {
                # Only accept JSON responses
                "Accept": "application/json",
                # Only accept UTF-8 encoded data
                "Accept-Charset": "utf-8",
                # Always sending JSON
                "Content-Type": "application/json",
                # Set our own custom User-Agent string
                "User-Agent": "ultron8.client/{0}".format(__version__),
            }
        )
        self.base_url = self.get_api_endpoint()
        self.two_factor_auth_cb = None
        self.request_counter = 0

    def get_api_endpoint(self) -> str:
        return get_api_endpoint()

    @property
    def timeout(self) -> Tuple[int, int]:
        """Return the timeout tuple as expected by Requests"""
        return (self.default_connect_timeout, self.default_read_timeout)

    def basic_auth(self, username: Optional[str], password: Optional[str]) -> None:
        """Set the Basic Auth credentials on this Session.

        :param str username: Your UltronAPI username
        :param str password: Your UltronAPI password
        """
        if not (username and password):
            return

        self.auth = BasicAuth(username, password)

    def build_url(self, *args, **kwargs) -> str:
        """Build a new API url from scratch."""
        parts = [kwargs.get("base_url") or self.base_url]
        parts.extend(args)
        parts = [str(p) for p in parts]
        key = tuple(parts)
        logger.info("Building a url from %s", key)
        if key not in __url_cache__:
            logger.info("Missed the cache building the url")
            __url_cache__[key] = "/".join(parts)
        return __url_cache__[key]

    def handle_two_factor_auth(
        self,
        args: Union[Tuple[_ANY, str, str], Tuple[str, str]],
        kwargs: Dict[str, Union[bool, Tuple[int, int]]],
    ) -> Union[Mock, MagicMock]:
        """Handler for when the user has 2FA turned on."""
        headers = kwargs.pop("headers", {})
        headers.update({"X-UltronAPI-OTP": str(self.two_factor_auth_cb())})
        kwargs.update(headers=headers)
        return super(UltronSession, self).request(*args, **kwargs)

    def has_auth(self):
        """Check for whether or not the user has authentication configured."""
        return self.auth or self.headers.get("Authorization")

    # def oauth2_auth(self, client_id, client_secret):
    #     """Use OAuth2 for authentication.

    #     It is suggested you install requests-oauthlib to use this.

    #     :param str client_id: Client ID retrieved from UltronAPI
    #     :param str client_secret: Client secret retrieved from UltronAPI
    #     """
    #     raise NotImplementedError("These features are not implemented yet")

    def request(self, *args, **kwargs) -> Union[Mock, Response]:
        """Make a request, count it, and handle 2FA if necessary."""
        kwargs.setdefault("timeout", self.timeout)
        response = super(UltronSession, self).request(*args, **kwargs)
        self.request_counter += 1
        if requires_2fa(response) and self.two_factor_auth_cb:
            # No need to flatten and re-collect the args in
            # handle_two_factor_auth
            new_response = self.handle_two_factor_auth(args, kwargs)
            new_response.history.append(response)
            response = new_response
        return response

    def retrieve_client_credentials(self) -> Union[Tuple[None, None], Tuple[str, str]]:
        """Return the client credentials.

        :returns: tuple(client_id, client_secret)
        """
        client_id = self.params.get("client_id")
        client_secret = self.params.get("client_secret")
        return (client_id, client_secret)

    def two_factor_auth_callback(
        self, callback: Optional[Union[Callable, int]]
    ) -> None:
        """Register our 2FA callback specified by the user."""
        if not callback:
            return

        if not isinstance(callback, abc_collections.Callable):
            raise ValueError("Your callback should be callable")

        self.two_factor_auth_cb = callback

    def token_auth(self, token: Optional[str]) -> None:
        """Use an application token for authentication.

        :param str token: Application token retrieved from UltronAPI's
            /authorizations endpoint
        """
        if not token:
            return

        self.auth = TokenAuth(token)

    def app_bearer_token_auth(self, headers, expire_in):
        """Authenticate as an App to be able to view its metadata."""
        if not headers:
            return

        self.auth = AppBearerTokenAuth(headers, expire_in)

    def app_installation_token_auth(self, json):
        """Use an access token generated by an App's installation."""
        if not json:
            return

        self.auth = AppInstallationTokenAuth(json["token"], json["expires_at"])

    @contextmanager
    def temporary_basic_auth(self, *auth) -> Iterator[None]:
        """Allow us to temporarily swap out basic auth credentials."""
        old_basic_auth = self.auth
        old_token_auth = self.headers.get("Authorization")

        self.basic_auth(*auth)
        yield

        self.auth = old_basic_auth
        if old_token_auth:
            self.headers["Authorization"] = old_token_auth

    @contextmanager
    def no_auth(self) -> Iterator[None]:
        """Unset authentication temporarily as a context manager."""
        old_basic_auth, self.auth = self.auth, None
        old_token_auth = self.headers.pop("Authorization", None)

        yield

        self.auth = old_basic_auth
        if old_token_auth:
            self.headers["Authorization"] = old_token_auth


def _utcnow():
    return datetime.datetime.now(dateutil.tz.UTC)


class AppInstallationTokenAuth(TokenAuth):
    """Use token authentication but throw an exception on expiration."""

    def __init__(self, token, expires_at):
        """Set-up our authentication handler."""
        super(AppInstallationTokenAuth, self).__init__(token)
        self.expires_at_str = expires_at
        self.expires_at = dateutil.parser.parse(expires_at)

    def __repr__(self):
        """Return a nice view of the token in use."""
        return "app installation token {}... expiring at {}".format(
            self.token[:4], self.expires_at_str
        )

    @property
    def expired(self):
        """Indicate whether our token is expired or not."""
        now = _utcnow()
        return now > self.expires_at

    def __call__(self, request):
        """Add the authorization header and format it."""
        if self.expired:
            raise AppInstallationTokenExpired(
                "Your app installation token expired at {}".format(self.expires_at_str)
            )
        return super(AppInstallationTokenAuth, self).__call__(request)


class AppBearerTokenAuth(TokenAuth):
    """Use JWT authentication but throw an exception on expiration."""

    header_format_str = "Bearer {}"

    def __init__(self, token, expire_in):
        """Set-up our authentication handler."""
        super(AppBearerTokenAuth, self).__init__(token)
        expire_in = datetime.timedelta(seconds=expire_in)
        self.expires_at = _utcnow() + expire_in

    def __repr__(self):
        """Return a helpful view of the token."""
        return "app bearer token {} expiring at {}".format(
            self.token[:4], str(self.expires_at)
        )

    @property
    def expired(self):
        """Indicate whether our token is expired or not."""
        now = _utcnow()
        return now > self.expires_at

    def __call__(self, request):
        """Add the authorization header and format it."""
        if self.expired:
            raise AppTokenExpired(
                "Your app token expired at {}".format(str(self.expires_at))
            )
        return super(AppBearerTokenAuth, self).__call__(request)


##################################################################################################
#      SESSION STUFF ENDS
##################################################################################################
