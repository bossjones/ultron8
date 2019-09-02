from __future__ import absolute_import
from ultron8.exceptions import UltronBaseException

__all__ = [
    "ParameterRenderingFailedException",
    "InvalidActionReferencedException",
    "InvalidActionParameterException",
]


class ParameterRenderingFailedException(UltronBaseException):
    pass


class InvalidActionReferencedException(UltronBaseException):
    pass


class InvalidActionParameterException(UltronBaseException):
    pass
