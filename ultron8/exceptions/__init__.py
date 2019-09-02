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
