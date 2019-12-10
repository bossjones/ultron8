"""
supporting task functions
"""
import logging
import copy
import os
import sys


logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


# https://stackoverflow.com/questions/1871549/determine-if-python-is-running-inside-virtualenv
def is_venv():
    """[summary]

    Returns:
        [type] -- [description]
    """
    return hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )


def get_version(name):
    """[summary]

    Arguments:
        name {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    from ultron8 import __version__

    return __version__


def get_compose_env(c, loc="docker", name=None):
    """
    The variables are looked up in this priority: invoke.yaml dev.env variables, environment variables,
    If `name` is provided, it will look up for `name` in os.environ
        then it will try to load it if VAULT_{name} is defined
    Vault variables
    """
    env = copy.copy(c[loc]["env"])
    env["VERSION"] = get_version(c["name"])
    env["NAME"] = c["name"]

    # environment variables have priority over what's inside invoke.yaml
    for key in env:
        if key in os.environ:
            env[key] = os.getenv(key)

    if name:
        if name in env:
            return env[name]

    return env


def confirm():
    """
    Ask user to enter Y or N (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """
    answer = ""
    while answer not in ["y", "n"]:
        answer = input("Are you sure you want to execute this command [Y/N]? ").lower()
    return answer == "y"
