from __future__ import absolute_import
from ultron8.exceptions import UltronPluginException


class ActionRunnerException(UltronPluginException):
    pass


class ActionRunnerCreateError(ActionRunnerException):
    pass


class ActionRunnerDispatchError(ActionRunnerException):
    pass


class ActionRunnerPreRunError(ActionRunnerException):
    pass


class InvalidActionRunnerOperationError(ActionRunnerException):
    pass


class UnexpectedActionExecutionStatusError(ActionRunnerException):
    pass
