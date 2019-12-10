"""
supporting task functions
"""
import logging
import copy
import os
import sys
from getpass import getpass

# from keyrings.cryptfile.cryptfile import CryptFileKeyring


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


# SOURCE: https://git.corp.adobe.com/Evergreen/pops/blob/master/src/pops/tasks/libs/utils.py
# def confirm(ctx, msg="Are you sure you want to execute this command?"):
#     """
#     Ask user to enter Y or N (case-insensitive).
#     :return: True if the answer is Y.
#     :rtype: bool
#     """
#     if not ctx.ask_confirmation:
#         return True
#     answer = None
#     acceptable_answers = ["y", "n", ""] if ctx.default_confirmation else ["y", "n"]
#     display_options = "[Y/n]" if ctx.default_confirmation else "[y/n]"
#     while answer not in acceptable_answers:
#         answer = input(f"{msg}\n{display_options} ").lower()
#         if ctx.default_confirmation and answer == "":
#             answer = "y"
#     return answer == "y"

# def get_keyring():
#     """
#     Build a CryptFileKeyring object
#     """
#     if os.environ.get('KEYRING_PASS', None) is None:
#         logger.error('KEYRING_PASS env variable not found')
#         raise RuntimeError('KEYRING_PASS environment variable was not defined')
#     cfk = CryptFileKeyring()
#     cfk.keyring_key = os.environ.get('KEYRING_PASS')
#     # this is needed for the keyring command
#     cfk.set_password('keyring-setting', 'password reference', 'password reference value')
#     return cfk

# def get_secret(env_var_name, message):
#     """
#     Ask the user to provide a secret.
#     If the environment variable with the name of `env_var_name` exists, the secret is set to that value
#     """
#     if os.environ.get(env_var_name, None) is None:
#         secret = getpass(message)
#         if not secret:
#             logger.error('Empty input.')
#             sys.exit(1)
#     else:
#         secret = os.environ.get(env_var_name)
#     return secret
