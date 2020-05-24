from __future__ import absolute_import

from ultron8.exceptions import UltronBaseException


class UnsupportedMetaException(UltronBaseException):
    pass


class ParseException(ValueError):
    pass
