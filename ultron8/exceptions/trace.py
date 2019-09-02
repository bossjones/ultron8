from __future__ import absolute_import
from ultron8.exceptions import UltronBaseException
from ultron8.exceptions.db import UltronDBObjectNotFoundError


class UniqueTraceNotFoundException(UltronBaseException):
    pass


class TraceNotFoundException(UltronDBObjectNotFoundError):
    pass
