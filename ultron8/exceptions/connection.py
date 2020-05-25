class UnknownHostException(Exception):
    """Raised when a host is unknown (dns failure)"""


class ConnectionErrorException(Exception):
    """Raised on error connecting (connection refused/timed out)"""


class AuthenticationException(Exception):
    """Raised on authentication error (user/password/ssh key error)"""
