from ultron8.exceptions import UltronBaseException


class InvalidTokenError(UltronBaseException):
    pass


class InvalidSignatureError(UltronBaseException):
    pass
