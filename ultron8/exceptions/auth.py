from __future__ import absolute_import
from ultron8.exceptions import UltronBaseException
from ultron8.exceptions.db import UltronDBObjectNotFoundError

__all__ = [
    "TokenNotProvidedError",
    "TokenNotFoundError",
    "TokenExpiredError",
    "TTLTooLargeException",
    "ApiKeyNotProvidedError",
    "ApiKeyNotFoundError",
    "MultipleAuthSourcesError",
    "NoAuthSourceProvidedError",
    "NoNicknameOriginProvidedError",
    "UserNotFoundError",
    "AmbiguousUserError",
    "NotServiceUserError",
]


class TokenNotProvidedError(UltronBaseException):
    pass


class TokenNotFoundError(UltronDBObjectNotFoundError):
    pass


class TokenExpiredError(UltronBaseException):
    pass


class TTLTooLargeException(UltronBaseException):
    pass


class ApiKeyNotProvidedError(UltronBaseException):
    pass


class ApiKeyNotFoundError(UltronDBObjectNotFoundError):
    pass


class ApiKeyDisabledError(UltronDBObjectNotFoundError):
    pass


class MultipleAuthSourcesError(UltronBaseException):
    pass


class NoAuthSourceProvidedError(UltronBaseException):
    pass


class NoNicknameOriginProvidedError(UltronBaseException):
    pass


class UserNotFoundError(UltronBaseException):
    pass


class AmbiguousUserError(UltronBaseException):
    pass


class NotServiceUserError(UltronBaseException):
    pass
