"""
ultron8.encoding
~~~~~~~~~~~~~~
Provides utility functions that are consumed internally by Ultron8
which depend on extremely few external helpers (such as compat)
"""

import codecs
import locale

# from .compat import is_py2, builtin_str, str

# NOTE: python 3 convert byte string variable to regular string
# http://stackoverflow.com/questions/31058055/python-3-convert-byte-string-variable-to-regular-string


def bytesting_to_string(a_bytestring):
    # If we have a byte instead of a strng, decode to str type
    if isinstance(a_bytestring, bytes):
        a_bytestring = a_bytestring.decode("utf-8")

    return a_bytestring


def locale_decode(bytestr):
    # try:
    # PY2: text_type = unicode  # noqa
    # In [8]: unicode(bytestr)
    # ---------------------------------------------------------------------------
    # UnicodeDecodeError                        Traceback (most recent call last)
    # <ipython-input-8-819e1ae0f3d4> in <module>()
    # ----> 1 unicode(bytestr)
    #
    # UnicodeDecodeError: 'ascii' codec can't decode byte 0xe9 in position 20: ordinal not in range(128)

    # PY3: text_type = str
    #      str(bytestr) = "b'[Errno 98] Adresse d\\xe9j\\xe0 utilis\\xe9e'"
    return str(bytestr)
    # except UnicodeError:
    #     return bytes(bytestr).decode(locale.getpreferredencoding())


def to_native_string(string, encoding="ascii"):
    """Given a string object, regardless of type, returns a representation of
    that string in the native string type, encoding and decoding where
    necessary. This assumes ASCII unless told otherwise.
    """
    # NOTE: @source: https://github.com/kennethreitz/requests/blob/5c4549493b35f5dbb084d029eaf12b6c7ce22579/requests/_internal_utils.py
    if isinstance(string, str):
        out = string
    else:
        out = string.decode(encoding)

    return out


def unicode_is_ascii(u_string):
    """Determine if unicode string only contains ASCII characters.
    :param str u_string: unicode string to check. Must be unicode
        and not Python 2 `str`.
    :rtype: bool
    """
    assert isinstance(u_string, str)
    try:
        u_string.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False
