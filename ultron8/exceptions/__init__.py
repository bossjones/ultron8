"""Ultron Exceptions Module."""


class UltronBaseException(Exception):
    """
        The root of the exception class hierarchy for all
        Ultron server exceptions.

        For exceptions raised by plug-ins, see UltronPluginException
        class.
    """

    pass


class UltronPluginException(UltronBaseException):
    """
        The root of the exception class hierarchy for all
        exceptions that are defined as part of a Ultron
        plug-in API.

        It is recommended that each API define a root exception
        class for the API. This root exception class for the
        API should inherit from the UltronPluginException
        class.
    """

    pass


###########################
class InvalidEntityFormatError(UltronBaseException):
    """When an invalid formatted entity is encountered."""

    pass


class NoEntitySpecifiedError(UltronBaseException):
    """When no entity is specified."""

    pass


class TemplateError(UltronBaseException):
    """Error during template rendering."""

    def __init__(self, exception):
        """Initalize the error."""
        super().__init__("{}: {}".format(exception.__class__.__name__, exception))


class FindError(UltronBaseException):
    def __init__(self, message, errno=None):
        super(FindError, self).__init__(message, errno)
        self.errno = errno


class DecodeError(Exception):
    """The base exception class for all decoding errors raised by this package."""


class NoBackendError(DecodeError):
    """The file could not be decoded by any backend. Either no backends are available or each available backend failed to decode the file."""


class MainRunnerError(Exception):
    pass


class MainRunnerAbortedError(MainRunnerError):
    pass


class MainRunnerTimeoutError(MainRunnerError):
    pass


class SubProcessError(Exception):
    pass


class TimeOutError(Exception):
    pass
