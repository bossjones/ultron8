# -*- coding: utf-8 -*-
"""Debugging module. Import these functions in pdb or jupyter notebooks to figure step through code execution."""
import logging

LOGGER = logging.getLogger(__name__)


def init_debugger():
    import sys

    from IPython.core.debugger import Tracer  # noqa
    from IPython.core import ultratb

    sys.excepthook = ultratb.FormattedTB(
        mode="Verbose", color_scheme="Linux", call_pdb=True, ostream=sys.__stdout__
    )


# source: http://blender.stackexchange.com/questions/1879/is-it-possible-to-dump-an-objects-properties-and-methods
def debug_dump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))


# NOTE: What is a lexer - A lexer is a software program that performs lexical analysis. Lexical analysis is the process of separating a stream of characters into different words, which in computer science we call 'tokens' . When you read my answer you are performing the lexical operation of breaking the string of text at the space characters into multiple words.
def dump_color(obj):
    # source: https://gist.github.com/EdwardBetts/0814484fdf7bbf808f6f
    from pygments import highlight

    # Module name actually exists, but pygments loads things in a strange manner
    from pygments.lexers import Python3Lexer  # pylint: disable=no-name-in-module
    from pygments.formatters.terminal256 import (
        Terminal256Formatter,
    )  # pylint: disable=no-name-in-module

    for attr in dir(obj):
        if hasattr(obj, attr):
            obj_data = "obj.%s = %s" % (attr, getattr(obj, attr))
            print(highlight(obj_data, Python3Lexer(), Terminal256Formatter()))


# SOURCE: https://github.com/j0nnib0y/gtao_python_wrapper/blob/9cdae5ce40f9a41775e29754b51325652584cf25/debug.py
def dump_magic(obj, magic=False):
    """Dumps every attribute of an object to the console.
    Args:
        obj (any object): object you want to dump
        magic (bool, optional): True if you want to output "magic" attributes (like __init__, ...)
    """
    for attr in dir(obj):
        if magic is True:
            print("obj.%s = %s" % (attr, getattr(obj, attr)))
        else:
            if not attr.startswith("__"):
                print("obj.%s = %s" % (attr, getattr(obj, attr)))


def get_pprint():
    import pprint

    # global pretty print for debugging
    pp = pprint.PrettyPrinter(indent=4)
    return pp


def pprint_color(obj):
    # source: https://gist.github.com/EdwardBetts/0814484fdf7bbf808f6f
    from pygments import highlight

    # Module name actually exists, but pygments loads things in a strange manner
    from pygments.lexers import PythonLexer  # pylint: disable=no-name-in-module
    from pygments.formatters.terminal256 import (
        Terminal256Formatter,
    )  # pylint: disable=no-name-in-module
    from pprint import pformat

    print(highlight(pformat(obj), PythonLexer(), Terminal256Formatter()))


# SOURCE: https://stackoverflow.com/questions/192109/is-there-a-built-in-function-to-print-all-the-current-properties-and-values-of-a
def dump_dir(obj):
    """Without arguments, return the list of names in the current local scope. With an argument, attempt to return a list of valid attributes for that object."""
    pp = get_pprint()
    l = dir(obj)
    print("dump_dir for object: {}".format(obj))
    pp.pprint(l)
    return l


def dump_dict(obj):
    pp = get_pprint()
    d = obj.__dict__
    print("dump_dict for object: {}".format(obj))
    pp.pprint(d)
    return d


def dump_vars(obj):
    pp = get_pprint()
    print("dump_vars for object: {}".format(obj))
    v = vars(obj)
    pp.pprint(v)
    return v


def dump_all(obj):
    print("[run]--------------[dir(obj)]--------------")
    l = dump_dir(obj)
    print("[run]--------------[obj.__dict__]--------------")
    d = dump_dict(obj)
    print("[run]--------------[pp.pprint(vars(obj))]--------------")
    v = dump_vars(obj)
