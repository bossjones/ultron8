"""Ultron8 utils. Deals with all things at the file system level."""
from __future__ import absolute_import, unicode_literals

import argparse
import collections
import contextlib
import copy
import errno
import fcntl
import getpass
import io
import itertools
import logging
import math
import os
from pathlib import Path
import re
import select
import shutil
import signal
import stat
import subprocess
import sys
import time
import traceback
from urllib.parse import urlparse

from fastapi import HTTPException
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from starlette import status

LOGGER = logging.getLogger(__name__)

SEPARATOR_CHARACTER_DEFAULT = "-"
SEPARATOR_LENGTH_DEFAULT = 40

# SOURCE: python 3 OOP book
# def log_calls(func):
#     def wrapper(*args, **kwargs):
#         now = time.time()
#         print("Calling {0} with {1} and {2}".format(func.__name__, args, kwargs))
#         return_value = func(*args, **kwargs)
#         print("Executed {0} in {1}ms".format(func.__name__, time.time() - now))
#         return return_value
#     return wrapper


def maybe_decode(maybe_string):
    if type(maybe_string) is bytes:
        return maybe_string.decode()
    return maybe_string


def maybe_encode(maybe_bytes: str) -> bytes:
    if type(maybe_bytes) is not bytes:
        return maybe_bytes.encode()
    return maybe_bytes


def next_or_none(iterable):
    try:
        return next(iterable)
    except StopIteration:
        pass


# @contextlib.contextmanager
# def flock(fd):
#     close = False
#     if isinstance(fd, str):
#         fd = open(fd, "a")
#         close = True

#     try:
#         fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
#     except BlockingIOError as e:  # locked by someone else
#         LOGGER.debug(f"Locked by another process: {fd}")
#         raise e

#     try:
#         yield
#     finally:
#         fcntl.lockf(fd, fcntl.LOCK_UN)
#         if close:
#             fd.close()


# @contextlib.contextmanager
# def chdir(path):
#     cwd = os.getcwd()
#     os.chdir(path)
#     try:
#         yield
#     finally:
#         os.chdir(cwd)


# @contextlib.contextmanager
# def signals(signal_map):
#     orig_map = {}
#     for signum, handler in signal_map.items():
#         orig_map[signum] = signal.signal(signum, handler)

#     try:
#         yield
#     finally:
#         for signum, handler in orig_map.items():
#             signal.signal(signum, handler)


# ------------------------------------------------


# def mkdir_p(path):
#     p = Path(path)
#     p.mkdir(parents=True, exist_ok=True)
#     d = dir_exists(path)
#     LOGGER.info("Verify mkdir_p ran: {}".format(d))


# def dir_exists(path):
#     p = Path(path)
#     if not p.is_dir():
#         LOGGER.error("This is not a dir: {}".format(path))
#         return False
#     return True


# def mkdir_if_does_not_exist(path):
#     if not dir_exists(path):
#         LOGGER.error("Dir does not exist, creating ... : {}".format(path))
#         mkdir_p(path)
#         return True
#     return False


# SOURCE: https://github.com/edx/tubular/blob/2dcb3f7f420afbf6bd85fda91911e90eab668e52/tubular/utils/__init__.py
def envvar_get_int(var_name, default):
    """Grab an environment variable and return it as an integer. If the environment variable does not exist, return the default."""

    return int(os.environ.get(var_name, default))


def get_sys_module():
    import sys  # pylint:disable=reimported,import-outside-toplevel

    return sys


def get_itertools_module():
    import itertools  # pylint:disable=reimported,import-outside-toplevel

    return itertools


# SOURCE: https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch14s08.html
def _whoami():
    """By calling sys._getframe(1), you can get this information for the caller of the current function."""
    sys = get_sys_module()
    return sys._getframe(1).f_code.co_name


def callersname():
    sys = get_sys_module()
    return sys._getframe(2).f_code.co_name


def print_line_seperator(
    value: str,
    length: int = SEPARATOR_LENGTH_DEFAULT,
    char: str = SEPARATOR_CHARACTER_DEFAULT,
):
    output = value

    if len(value) < length:
        #   Update length based on insert length, less a space for margin.
        length -= len(value) + 2
        #   Halve the length and floor left side.
        left = math.floor(length / 2)
        right = left
        #   If odd number, add dropped remainder to right side.
        if length % 2 != 0:
            right += 1

        #   Surround insert with separators.
        output = f"{char * left} {value} {char * right}"

    print_output(output)


def print_output(*args, sep: str = " ", end: str = "\n"):
    print(*args, sep=sep, end=end)


# SOURCE: https://gist.github.com/89465127/5776892
def create_dict_from_filter(d, white_list):
    """Filter by key"""
    return {k: v for k, v in filter(lambda t: t[0] in white_list, d.items())}


# Higher level functions
def remove(path):
    def remove_readonly(func, path, _):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    shutil.rmtree(path, onerror=remove_readonly)


# NAME: Python filter nested dict given list of key names
# https://stackoverflow.com/questions/23230947/python-filter-nested-dict-given-list-of-key-names
def fltr(node, whitelist):
    """
    returns a new object rather than modifying the old one (and handles filtering on non-leaf nodes).
    Example Usage: `fltr(x, ['dropdown_value', 'nm_field', 'url_app', 'dt_reg'])`
    """
    if isinstance(node, dict):
        retVal = {}
        for key in node:
            if key in whitelist:
                retVal[key] = copy.deepcopy(node[key])
            elif isinstance(node[key], list) or isinstance(node[key], dict):
                child = fltr(node[key], whitelist)
                if child:
                    retVal[key] = child
        if retVal:
            return retVal
        else:
            return None
    elif isinstance(node, list):
        retVal = []
        for entry in node:
            child = fltr(entry, whitelist)
            if child:
                retVal.append(child)
        if retVal:
            return retVal
        else:
            return None


###############


# SOURCE: https://github.com/ARMmbed/mbed-cli/blob/f168237fabd0e32edcb48e214fc6ce2250046ab3/test/util.py
# Process execution
class ProcessException(Exception):
    pass


# Clone everything that doesnt exist
def git_clone(repo_url, dest, sha="master"):
    # First check if folder exists
    if not os.path.exists(dest):
        # check if folder is a git repo
        if scm(dest) != "git":
            clone_cmd = "git clone {repo} {dest}".format(repo=repo_url, dest=dest)
            _popen_stdout(clone_cmd)

            # CD to directory
            with cd(dest):
                checkout_cmd = "git checkout {sha}".format(sha=sha)
                _popen_stdout(checkout_cmd)
    else:
        # check if folder is a git repo
        if scm(dest) == "git":
            git_pull_rebase(repo_url, dest, sha)


# make sure configs are up to date
def git_pull_rebase(repo_url, dest, sha="master"):
    # First check if folder exists
    if os.path.exists(dest):
        # check if folder is a git repo
        if scm(dest) == "git":
            # first checkout correct version
            with cd(dest):
                checkout_cmd = "git checkout {sha}".format(sha=sha)
                _popen_stdout(checkout_cmd)

                # Then pull --rebase
                git_pull_rebase_cmd = "git pull --rebase"
                _popen_stdout(git_pull_rebase_cmd)
    else:
        raise RuntimeError(
            "Sorry it seems git checkout of '{repo_url}' on sha '{sha}' to destination '{dest}' did not work!".format(
                repo_url=repo_url, sha=sha, dest=dest
            )
        )


# Directory navigation
@contextlib.contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(newdir)
    try:
        yield
    finally:
        os.chdir(prevdir)


def scm(dir=None):
    if not dir:
        dir = os.getcwd()

    if os.path.isdir(os.path.join(dir, ".git")):
        return "git"
    elif os.path.isdir(os.path.join(dir, ".hg")):
        return "hg"


def _popen(cmd_arg):
    devnull = open("/dev/null")
    cmd = subprocess.Popen(cmd_arg, stdout=subprocess.PIPE, stderr=devnull, shell=True)
    retval = cmd.stdout.read().strip()
    err = cmd.wait()
    cmd.stdout.close()
    devnull.close()
    if err:
        raise RuntimeError("Failed to close %s stream" % cmd_arg)
    return retval


def _popen_stdout(cmd_arg, cwd=None):
    # if passing a single string, either shell mut be True or else the string must simply name the program to be executed without specifying any arguments
    cmd = subprocess.Popen(
        cmd_arg,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=cwd,
        bufsize=4096,
        shell=True,
    )
    Console.message("BEGIN: {}".format(cmd_arg))
    # output, err = cmd.communicate()

    for line in iter(cmd.stdout.readline, b""):
        # Print line
        _line = line.rstrip()
        Console.message(">>> {}".format(_line.decode("utf-8")))

    Console.message("END: {}".format(cmd_arg))


class Console:  # pylint: disable=too-few-public-methods

    quiet = False

    @classmethod
    def message(cls, str_format, *args):
        if cls.quiet:
            return

        if args:
            print(str_format % args)
        else:
            print(str_format)

        # Flush so that messages are printed at the right time
        # as we use many subprocesses.
        sys.stdout.flush()


def pquery(command, stdin=None, **kwargs):
    # SOURCE: https://github.com/ARMmbed/mbed-cli/blob/f168237fabd0e32edcb48e214fc6ce2250046ab3/test/util.py
    # Example:
    print(" ".join(command))
    proc = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs
    )
    stdout, _ = proc.communicate(stdin)

    if proc.returncode != 0:
        raise ProcessException(proc.returncode)

    return stdout.decode("utf-8")


# # SOURCE: https://github.com/danijar/mindpark/blob/master/mindpark/utility/other.py
# def color_stack_trace():

#     def excepthook(type_, value, trace):
#         text = ''.join(traceback.format_exception(type_, value, trace))
#         try:
#             from pygments import highlight
#             from pygments.lexers import get_lexer_by_name
#             from pygments.formatters import TerminalFormatter
#             lexer = get_lexer_by_name('pytb', stripall=True)
#             formatter = TerminalFormatter()
#             sys.stderr.write(highlight(text, lexer, formatter))
#         except Exception:
#             sys.stderr.write(text)
#             sys.stderr.write('Failed to colorize the traceback.')

#     sys.excepthook = excepthook
#     setup_thread_excepthook()


# def setup_thread_excepthook():
#     """
#     Workaround for `sys.excepthook` thread bug from:
#     http://bugs.python.org/issue1230540
#     Call once from the main thread before creating any threads.
#     """
#     init_original = threading.Thread.__init__

#     def init(self, *args, **kwargs):
#         init_original(self, *args, **kwargs)
#         run_original = self.run

#         def run_with_except_hook(*args2, **kwargs2):
#             try:
#                 run_original(*args2, **kwargs2)
#             except Exception:
#                 sys.excepthook(*sys.exc_info())

#         self.run = run_with_except_hook

#     threading.Thread.__init__ = init

# SOURCE: https://github.com/bergran/fast-api-project-template/blob/master/README.md
def get_object_or_404(qs):
    try:
        return qs.one()
    except MultipleResultsFound:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


# SOURCE: https://github.com/bergran/fast-api-project-template/blob/master/README.md
def get_object(qs):
    try:
        return qs.one()
    except MultipleResultsFound:
        return None
    except NoResultFound:
        return None


# from unittest import TestCase
# SOURCE: https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
def dict_merge(dct, merge_dct, add_keys=True):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.

    This version will return a copy of the dictionary and leave the original
    arguments untouched.

    The optional argument ``add_keys``, determines whether keys which are
    present in ``merge_dict`` but not ``dct`` should be included in the
    new dict.

    Args:
        dct (dict) onto which the merge is executed
        merge_dct (dict): dct merged into dct
        add_keys (bool): whether to add new keys

    Returns:
        dict: updated dict
    """
    dct = dct.copy()
    if not add_keys:
        merge_dct = {k: merge_dct[k] for k in set(dct).intersection(set(merge_dct))}

    for k, v in merge_dct.items():
        if (
            k in dct
            and isinstance(dct[k], dict)
            and isinstance(merge_dct[k], collections.Mapping)
        ):
            dct[k] = dict_merge(dct[k], merge_dct[k], add_keys=add_keys)
        else:
            dct[k] = merge_dct[k]

    return dct
