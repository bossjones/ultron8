import logging
import re

import ipaddr

LOG = logging.getLogger(__name__)

__all__ = ["is_ipv4", "is_ipv6", "split_host_port"]

BRACKET_PATTERN = r"^\[.*\]"  # IPv6 bracket pattern to specify port
COMPILED_BRACKET_PATTERN = re.compile(BRACKET_PATTERN)

HOST_ONLY_IN_BRACKET = r"^\[.*\]$"
COMPILED_HOST_ONLY_IN_BRACKET_PATTERN = re.compile(HOST_ONLY_IN_BRACKET)


def is_ipv6(ip_str):
    """
    Validate whether given string is IPv6.

    :param ip_str: String to validate.
    :type ip_str: ``str``

    :rtype: ``bool``
    """
    try:
        addr = ipaddr.IPAddress(ip_str)
        return addr.version == 6
    except:
        return False


def is_ipv4(ip_str):
    """
    Validate whether given string is IPv4.

    :param ip_str: String to validate.
    :type ip_str: ``str``

    :rtype: ``bool``
    """
    try:
        addr = ipaddr.IPAddress(ip_str)
        return addr.version == 4
    except:
        return False


def split_host_port(host_str):
    """
    Split host_str into host and port.
    Can handle IPv4, IPv6, hostname inside or outside brackets.

    Note: If you want to specify a port with IPv6, you definitely
    should enclose IP address within [].

    :param host_str: Host port string.
    :type host_str: ``str``

    :return: Hostname (string), port (int) tuple. Raises exception on invalid port.
    :rtype: ``tuple`` of ``str`` and ``int``
    """

    hostname = host_str
    port = None

    # If it's simple IPv6 or IPv4 address, return here.
    if is_ipv6(host_str) or is_ipv4(host_str):
        return (hostname, port)

    # Check if it's square bracket style.
    match = COMPILED_BRACKET_PATTERN.match(host_str)
    if match:
        LOG.debug("Square bracket style.")
        # Check if square bracket style no port.
        match = COMPILED_HOST_ONLY_IN_BRACKET_PATTERN.match(host_str)
        if match:
            hostname = match.group().strip("[]")
            return (hostname, port)

        hostname, separator, port = hostname.rpartition(":")
        try:
            LOG.debug(
                "host_str: %s, hostname: %s port: %s" % (host_str, hostname, port)
            )
            port = int(port)
            hostname = hostname.strip("[]")
            return (hostname, port)
        except:
            raise Exception("Invalid port %s specified." % port)
    else:
        LOG.debug("Non-bracket address. host_str: %s" % host_str)
        if ":" in host_str:
            LOG.debug("Non-bracket with port.")
            hostname, separator, port = hostname.rpartition(":")
            try:
                port = int(port)
                return (hostname, port)
            except:
                raise Exception("Invalid port %s specified." % port)

    return (hostname, port)
