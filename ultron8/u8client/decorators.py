"""This module provides decorators to the rest of the library."""
# pylint: disable=logging-not-lazy

from functools import wraps
from requests.models import Response
import os
from io import BytesIO as StringIO

from ultron8.exceptions.client import (
    # AppInstallationTokenExpired,
    # AppTokenExpired,
    # AuthenticationFailed,
    # BadRequest,
    # CardHasNoContentUrl,
    # ClientError,
    # Conflict,
    # ConnectionError,
    # ForbiddenError,
    # GeneratedTokenExpired,
    # IncompleteResponse,
    # MethodNotAllowed,
    # MissingAppAuthentication,
    MissingAppBearerAuthentication,
    MissingAppInstallationAuthentication,
    # NotAcceptable,
    # NotFoundError,
    # NotRefreshable,
    # ResponseError,
    # ServerError,
    # TransportError,
    # UltronClientError,
    # UltronClientException,
    # UnavailableForLegalReasons,
    # UnexpectedResponse,
    # UnprocessableEntity,
    # UnprocessableResponseBody,
)


class RequestsStringIO(StringIO):
    """Shim compatibility for string IO."""

    def read(self, n=-1, *args, **kwargs):
        """Ignore extra args and kwargs."""
        # StringIO is an old-style class, so can't use super
        return StringIO.read(self, n)


def requires_auth(func):
    """Decorator to note which object methods require authorization."""

    @wraps(func)
    def auth_wrapper(self, *args, **kwargs):
        if hasattr(self, "session") and self.session.has_auth():
            return func(self, *args, **kwargs)
        else:
            from ultron8.exceptions.client import error_for

            # Mock a 401 response
            r = generate_fake_error_response('{"message": "Requires authentication"}')
            raise error_for(r)

    return auth_wrapper


def requires_basic_auth(func):
    """Specific (basic) authentication decorator.

    This is used to note which object methods require username/password
    authorization and won't work with token based authorization.

    """

    @wraps(func)
    def auth_wrapper(self, *args, **kwargs):
        if hasattr(self, "session") and self.session.auth:
            return func(self, *args, **kwargs)
        else:
            from ultron8.exceptions.client import error_for

            # Mock a 401 response
            r = generate_fake_error_response(
                '{"message": "Requires username/password authentication"}'
            )
            raise error_for(r)

    return auth_wrapper


def requires_app_credentials(func):
    """Require client_id and client_secret to be associated.

    This is used to note and enforce which methods require a client_id and
    client_secret to be used.

    """

    @wraps(func)
    def auth_wrapper(self, *args, **kwargs):
        client_id, client_secret = self.session.retrieve_client_credentials()
        if client_id and client_secret:
            return func(self, *args, **kwargs)
        else:
            from ultron8.exceptions.client import error_for

            # Mock a 401 response
            r = generate_fake_error_response(
                '{"message": "Requires username/password authentication"}'
            )
            raise error_for(r)

    return auth_wrapper


def requires_app_bearer_auth(func):
    """Require the use of application authentication.

    .. versionadded:: 1.2.0
    """

    @wraps(func)
    def auth_wrapper(self, *args, **kwargs):
        # TODO: Do we need to declare this here or can we do it at the top level?
        # from . import session
        from ultron8.u8client import session

        if isinstance(self.session.auth, session.AppBearerTokenAuth):
            return func(self, *args, **kwargs)
        else:
            # from . import exceptions

            raise MissingAppBearerAuthentication(
                "This method requires Ultron8 App authentication."
            )

    return auth_wrapper


def requires_app_installation_auth(func):
    """Require the use of App's installation authentication.

    .. versionadded:: 1.2.0
    """

    @wraps(func)
    def auth_wrapper(self, *args, **kwargs):
        # TODO: Do we need to declare this here or can we do it at the top level?
        # from . import session
        from ultron8.u8client import session

        if isinstance(self.session.auth, session.AppInstallationTokenAuth):
            return func(self, *args, **kwargs)
        else:
            # from . import exceptions

            raise MissingAppInstallationAuthentication(
                "This method requires Ultron8 App authentication."
            )

    return auth_wrapper


def generate_fake_error_response(msg, status_code=401, encoding="utf-8"):
    """Generate a fake Response from requests."""
    r = Response()
    r.status_code = status_code
    r.encoding = encoding
    r.raw = RequestsStringIO(msg.encode())
    r._content_consumed = True
    r._content = r.raw.read()
    return r


# Use mock decorators when generating documentation, so all functino signatures
# are displayed correctly
if os.getenv("GENERATING_DOCUMENTATION", None) == "github3":
    requires_auth = requires_basic_auth = lambda x: x  # noqa  # (No coverage)
