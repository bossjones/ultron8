"""All exceptions for the ultron8.client library."""
# pylint: disable=unnecessary-pass
from __future__ import absolute_import

from typing import Any, List

from requests.models import Response

from ultron8.exceptions import UltronBaseException


class UltronClientException(Exception):
    """The base exception class.

    .. versionadded:: 1.0.0

        Necessary to handle pre-response exceptions

    """


class GeneratedTokenExpired(UltronClientException):
    """This exception is used to prevent an expired token from being used.

    .. versionadded:: 1.2.0
    """


class AppInstallationTokenExpired(GeneratedTokenExpired):
    """This exception is used to prevent an expired token from being used.

    .. versionadded:: 1.2.0
    """


class AppTokenExpired(GeneratedTokenExpired):
    """This exception is used to prevent an expired token from being used.

    .. versionadded:: 1.2.0
    """


class MissingAppAuthentication(UltronClientException):
    """Raised when user tries to call a method that requires app auth.

    .. versionadded:: 1.2.0
    """


class MissingAppBearerAuthentication(MissingAppAuthentication):
    """Raised when user tries to call a method that requires app auth.

    .. versionadded:: 1.2.0
    """


class MissingAppInstallationAuthentication(MissingAppAuthentication):
    """Raised when user tries to call a method that requires app installation.

    .. versionadded:: 1.2.0
    """


class CardHasNoContentUrl(UltronClientException):
    """Raised when attempting a card has no ``content_url``.

    We use this in methods to retrieve the underlying issue or pull request
    based on the ``content_url``.

    .. versionadded:: 1.3.0
    """


class UltronClientError(UltronClientException):
    """The base exception class for all response-related exceptions.

    .. versionchanged:: 1.0.0

        This now inherits from :class:`~github3.exceptions.UltronClientException`

    .. attribute:: response

        The response object that triggered the exception

    .. attribute:: code

        The response's status code

    .. attribute:: errors

        The list of errors (if present) returned by UltronClient's API
    """

    def __init__(self, resp: Response) -> None:
        """Initialize our exception class."""
        super(UltronClientError, self).__init__(resp)
        #: Response code that triggered the error
        self.response = resp
        self.code = resp.status_code
        self.errors = []
        try:
            error = resp.json()
            #: Message associated with the error
            self.msg = error.get("message")
            #: List of errors provided by UltronClient
            if error.get("errors"):
                self.errors = error.get("errors")
        except Exception:  # Amazon S3 error
            self.msg = resp.content or "[No message]"

    def __repr__(self):
        return "<{0} [{1}]>".format(self.__class__.__name__, self.msg or self.code)

    def __str__(self):
        return "{0} {1}".format(self.code, self.msg)

    @property
    def message(self):
        """The actual message returned by the API."""
        return self.msg


class IncompleteResponse(UltronClientError):
    """Exception for a response that doesn't have everything it should.

    This has the same attributes as :class:`~github3.exceptions.UltronClientError`
    as well as

    .. attribute:: exception

        The original exception causing the IncompleteResponse exception
    """

    def __init__(self, json, exception):
        """Initialize our IncompleteResponse."""
        self.response = None
        self.code = None
        self.json = json
        self.errors = []
        self.exception = exception
        self.msg = (
            "The library was expecting more data in the response (%r)."
            " Either UltronClient modified it's response body, or your token"
            " is not properly scoped to retrieve this information."
        ) % (exception,)


class NotRefreshable(UltronClientException):
    """Exception to indicate that an object is not refreshable."""

    message_format = (
        '"{}" is not refreshable because the UltronClient API does '
        "not provide a URL to retrieve its contents from."
    )

    def __init__(self, object_name):
        """Initialize our NotRefreshable exception."""
        super(NotRefreshable, self).__init__(self.message_format.format(object_name))


class ResponseError(UltronClientError):
    """The base exception for errors stemming from UltronClient responses."""


class TransportError(UltronClientException):
    """Catch-all exception for errors coming from Requests.

    .. versionchanged:: 1.0.0

        Now inherits from :class:`~github3.exceptions.UltronClientException`.
    """

    msg_format = "An error occurred while making a request to UltronClient: {0}"

    def __init__(self, exception):
        """Initialize TransportError exception."""
        self.msg = self.msg_format.format(str(exception))
        super(TransportError, self).__init__(self, self.msg, exception)
        self.exception = exception

    def __str__(self):
        return "{0}: {1}".format(type(self.exception), self.msg)


class ConnectionError(TransportError):
    """Exception for errors in connecting to or reading data from UltronClient."""

    msg_format = "A connection-level exception occurred: {0}"


class UnexpectedResponse(ResponseError):
    """Exception class for responses that were unexpected."""


class UnprocessableResponseBody(ResponseError):
    """Exception class for response objects that cannot be handled."""

    def __init__(self, message: str, body: List[Any]) -> None:
        """Initialize UnprocessableResponseBody."""
        Exception.__init__(self, message)
        self.body = body
        self.msg = message

    def __repr__(self):
        return "<{0} [{1}]>".format("UnprocessableResponseBody", self.body)

    def __str__(self):
        return self.message


class BadRequest(ResponseError):
    """Exception class for 400 responses."""


class AuthenticationFailed(ResponseError):
    """Exception class for 401 responses.

    Possible reasons:

    - Need one time password (for two-factor authentication)
    - You are not authorized to access the resource
    """


class ForbiddenError(ResponseError):
    """Exception class for 403 responses.

    Possible reasons:

    - Too many requests (you've exceeded the ratelimit)
    - Too many login failures
    """


class NotFoundError(ResponseError):
    """Exception class for 404 responses."""


class MethodNotAllowed(ResponseError):
    """Exception class for 405 responses."""


class NotAcceptable(ResponseError):
    """Exception class for 406 responses."""


class Conflict(ResponseError):
    """Exception class for 409 responses.

    Possible reasons:

    - Head branch was modified (SHA sums do not match)
    """


class UnprocessableEntity(ResponseError):
    """Exception class for 422 responses."""


class ClientError(ResponseError):
    """Catch-all for 400 responses that aren't specific errors."""


class ServerError(ResponseError):
    """Exception class for 5xx responses."""


class UnavailableForLegalReasons(ResponseError):
    """Exception class for 451 responses."""


error_classes = {
    400: BadRequest,
    401: AuthenticationFailed,
    403: ForbiddenError,
    404: NotFoundError,
    405: MethodNotAllowed,
    406: NotAcceptable,
    409: Conflict,
    422: UnprocessableEntity,
    451: UnavailableForLegalReasons,
}


def error_for(response: Response) -> ServerError:
    """Return the appropriate initialized exception class for a response."""
    klass = error_classes.get(response.status_code)
    if klass is None:
        if 400 <= response.status_code < 500:
            klass = ClientError
        if 500 <= response.status_code < 600:
            klass = ServerError
    return klass(response)
