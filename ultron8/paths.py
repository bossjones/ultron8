"""Ultron8 path module. Deals with all things at the file system level."""

import logging
import os
import stat
import threading
import bisect
import stat
import sys

from ultron8 import exceptions
from ultron8.utils import encoding

from gettext import gettext as _

from pathlib import PosixPath, Path

import queue
import tempfile
import errno

import urllib  # noqa
from urllib.parse import (
    urlparse,
    urlunparse,
    quote_plus,
    unquote_plus,
    urlsplit,
    parse_qs,
    urlencode,
    quote,
    unquote,
    urljoin,
    urldefrag,
    urlunsplit,
)
from typing import Dict, List, Union

logger = logging.getLogger(__name__)


# class Paths(object):
#     @property
#     def base_path_dir(self):
#         return Path("/".join((os.path.expanduser("~"))))

#     @property
#     def ultron_config_dir(self):
#         return self.base_path_dir / ".config" / "ultron8"

#     @property
#     def ultron_config_path_file(self):
#         return self.ultron_config_dir / "config.yaml"

#     @property
#     def here_path_dir(self):
#         return Path(os.path.join(os.path.dirname(os.path.abspath(__file__))))

#     @property
#     def default_config_path_file(self):
#         return self.here_path_dir / "default_config.yaml"

#     @property
#     def data_home_path_dir(self):
#         return self.base_path_dir / ".local" / "share" / "ultron8" / "data"

#     @property
#     def build_path_dir(self):
#         return self.base_path_dir / ".local" / "share" / "ultron8" / "build"

#     @property
#     def cache_home_dir(self):
#         return self.base_path_dir / ".cache" / "ultron8"

#     # @property
#     # def assets_path(self):
#     #     return self.base_path_dir / 'assets'

#     # @property
#     # def template_path(self):
#     #     return self.base_path_dir / 'template'

# SOURCE:  https://realpython.com/python-pathlib/
def tree(directory: PosixPath) -> None:
    print(f"+ {directory}")
    for path in sorted(directory.rglob("*")):
        depth = len(path.relative_to(directory).parts)
        spacer = "    " * depth
        print(f"{spacer}+ {path.name}")


def is_readable_dir(path: str) -> Dict[str, Union[str, bool]]:
    """Check whether a path references a readable directory."""
    if not os.path.exists(path):
        return {"result": False, "message": "Path does not exist", "path": path}
    if not os.path.isdir(path):
        return {"result": False, "message": "Path is not a directory", "path": path}
    if not os.access(path, os.R_OK):
        return {"result": False, "message": "Directory is not readable", "path": path}
    return {"result": True}


def is_readable_file(path: str) -> Dict[str, Union[str, bool]]:
    """Check whether a path references a readable file."""
    if not os.path.exists(path):
        return {"result": False, "message": "Path does not exist", "path": path}
    if not os.path.isfile(path):
        return {"result": False, "message": "Path is not a file", "path": path}
    if not os.access(path, os.R_OK):
        return {"result": False, "message": "File is not readable", "path": path}
    return {"result": True}


# def is_writable_file(path):
#     """Check whether a path references a writable file."""
#     if not os.path.exists(path):
#         return {"result": False, "message": "Path does not exist", "path": path}
#     if not os.path.isfile(path):
#         return {"result": False, "message": "Path is not a file", "path": path}
#     if not os.access(path, os.R_OK):
#         return {"result": False, "message": "File is not writable", "path": path}
#     return {"result": True}


###############################################################################################################


def ensure_dir_exists(directory: str) -> None:
    # source: dcos-cli
    """If `directory` does not exist, create it.
    :param directory: path to the directory
    :type directory: string
    :rtype: None
    """

    res = is_readable_dir(directory)
    logger.info(f"Res: {res}")
    # import pdb;pdb.set_trace()

    if not res["result"]:
        logger.debug("Creating directory: %r", directory)

        try:
            os.makedirs(directory, 0o775)
        except os.error as e:
            raise Exception("Cannot create directory [{}]: {}".format(directory, e))


def ensure_file_exists(path: str, mode: int = 0o600) -> None:
    # source: dcos-cli
    """ Create file if it doesn't exist
    :param path: path of file to create
    :type path: str
    :rtype: None
    """

    res = is_readable_file(path)
    logger.info(f"Res: {res}")

    # if not os.path.exists(path):
    if not res["result"]:
        try:
            open(path, "w").close()
            os.chmod(path, mode)
        except IOError as e:
            raise Exception("Cannot create file [{}]: {}".format(path, e))


def get_permissions(path: str) -> str:
    return oct(stat.S_IMODE(os.stat(path).st_mode))


def enforce_file_permissions(path):
    # source: dcos-cli
    """Enforce 400 or 600 permissions on file
    :param path: Path to the TOML file
    :type path: str
    :rtype: None
    """
    res = is_readable_file(path)
    logger.info(f"Res: {res}")

    # if not os.path.isfile(path):
    if not res["result"]:
        raise Exception("Path [{}] is not a file".format(path))

    permissions = get_permissions(path)
    if permissions not in ["0o600", "0600", "0o400", "0400"]:
        if os.path.realpath(path) != path:
            path = "%s (pointed to by %s)" % (os.path.realpath(path), path)
        msg = (
            "Permissions '{}' for configuration file '{}' are too open. "
            "File must only be accessible by owner. "
            "Aborting...".format(permissions, path)
        )
        raise Exception(msg)


def get_parent_dir(path: str) -> str:
    logger.debug("get_parent_dir: {}".format(path))
    # In [13]: q.parent
    # Out[13]: PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug')
    p = Path(path)
    return p.parent.__str__()


def mkdir_p(path: str) -> None:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    d = dir_exists(path)
    logger.debug("Verify mkdir_p ran: {}".format(d))


def dir_exists(path: str) -> bool:
    p = Path(path)
    if not p.is_dir():
        logger.error("This is not a dir: {}".format(path))
        # NOTE this should raise a exception
    return p.is_dir()


def mkdir_if_does_not_exist(path: str) -> bool:
    if not dir_exists(path):
        mkdir_p(path)
        return True
    return False


def fname_exists(path: str) -> bool:
    p = Path(path)
    return p.exists()


# NOTE: Borrowed from Pitivi
# ------------------------------ URI helpers --------------------------------
# SOURCE: https://raw.githubusercontent.com/GNOME/pitivi/b2bbe6eef6d1e6d0fa5471d60004c62f936b3146/pitivi/utils/misc.py


def isWritable(path: str) -> bool:
    """Returns whether the file/path is writable."""
    try:
        res = is_readable_dir(path)
        if res["result"]:
            # The given path is an existing directory.
            # To properly check if it is writable, you need to use os.access.
            return os.access(path, os.W_OK)
        else:
            # The given path is supposed to be a file.
            # Avoid using open(path, "w"), as it might corrupt existing files.
            # And yet, even if the parent directory is actually writable,
            # open(path, "rw") will IOError if the file doesn't already exist.
            # Therefore, simply check the directory permissions instead:

            # path = 'file:///etc/fstab'
            # In [22]: os.path.dirname(path)
            # Out[22]: 'file:///etc'
            return os.access(os.path.dirname(path), os.W_OK)
            # In [23]: os.access(os.path.dirname(path), os.W_OK)
            # Out[23]: False
    except UnicodeDecodeError:
        unicode_error_dialog()


# def isReadable(path):
#     """Returns whether the file/path exists and is readable."""
#     try:
#         return os.path.exists(path) and os.access(path, os.R_OK)
#     except UnicodeDecodeError:
#         # message = _(
#         #     "The system's locale that you are using is not UTF-8 capable. "
#         #     "Unicode support is required for Python3 software like Pitivi. "
#         #     "Please correct your system settings; if you try to use Pitivi "
#         #     "with a broken locale, weird bugs will happen."
#         # )
#         # raise UnicodeDecodeError(message)
#         unicode_error_dialog()


def unicode_error_dialog():
    message = _(
        "The system's locale that you are using is not UTF-8 capable. "
        "Unicode support is required for Python3 software like Pitivi. "
        "Please correct your system settings; if you try to use Pitivi "
        "with a broken locale, weird bugs will happen."
    )

    logger.error(message)


def path_from_uri(raw_uri: Union[str, bytes]) -> str:
    """Returns a path that can be used with Python's os.path.
    Args:
        raw_uri (str, byte): The location to check.
    Return:
        (str): String containting path to file.
    """
    # NOTE: bossjones added
    # If we have a byte instead of a strng, decode to str type
    if isinstance(raw_uri, bytes):
        raw_uri = raw_uri.decode("utf-8")

    # assume: uri = b'file:///etc/fstab'
    uri = urlparse(raw_uri)
    # In [14]: urlparse(uri)
    # Out[14]: ParseResultBytes(scheme=b'file', netloc=b'', path=b'/etc/fstab', params=b'', query=b'', fragment=b'')
    assert uri.scheme == "file"
    # In [32]: unquote(uri.path)
    # Out[32]: '/etc/fstab'
    return unquote(uri.path)


def filename_from_uri(uri: Union[str, bytes]) -> str:
    """Returns a filename for display.
    Excludes the path to the file.
    Can be used in UI elements or to shorten debug statements.
    Args:
        uri (str, byte): Uri containing path to file (of type file://).
    Returns:
        (str): String containing file name from uri.
    """
    return os.path.basename(path_from_uri(uri))


def quote_uri(uri: bytes) -> str:
    """Encodes a URI according to RFC 2396.
    Does not touch the file:/// part.
    Args:
        uri (str, byte): Uri
    Returns:
        (str): string of uri
    """
    # NOTE: bossjones added
    # If we have a byte instead of a strng, decode to str type
    if isinstance(uri, bytes):
        uri = uri.decode("utf-8")

    # Split off the "file:///" part, if present.
    # In [34]: uri = 'file:///etc/fstab'
    #
    # In [35]: urlsplit(uri, allow_fragments=False)
    # Out[35]: SplitResult(scheme='file', netloc='', path='/etc/fstab', query='', fragment='')
    parts = urlsplit(uri, allow_fragments=False)
    # Make absolutely sure the string is unquoted before quoting again!
    # In [46]: raw_path = unquote(parts.path)
    #
    # In [47]: raw_path
    # Out[47]: '/etc/fstab'
    raw_path = unquote(parts.path)
    # For computing thumbnail md5 hashes in the media library, we must adhere to
    # RFC 2396. It is quite tricky to handle all corner cases, leave it to Gst:
    return f"file://{raw_path}"
    # In [48]: Gst.filename_to_uri(raw_path)
    # Out[48]: 'file:///etc/fstab'


def quantize(input: float, interval: float) -> float:
    # In Python 3, they made the / operator do a floating-point division, and added the // operator to do integer division (i.e. quotient without remainder);
    return (input // interval) * interval


def binary_search(elements: List[int], value: int) -> int:
    """Returns the index of the element closest to value.
    Args:
        elements (List): A sorted list.
    """
    if not elements:
        return -1
    closest_index = bisect.bisect_left(elements, value, 0, len(elements) - 1)
    element = elements[closest_index]
    closest_distance = abs(element - value)
    if closest_distance == 0:
        return closest_index
    for index in (closest_index - 1,):
        if index < 0:
            continue
        distance = abs(elements[index] - value)
        if closest_distance > distance:
            closest_index = index
            closest_distance = distance
    return closest_index


# ------------------------------ URI helpers --------------------------------


def path_to_uri(path: str) -> bytes:
    """
    Convert OS specific path to file:// URI.
    Accepts either unicode strings or bytestrings. The encoding of any
    bytestring will be maintained so that :func:`uri_to_path` can return the
    same bytestring.
    Returns a file:// URI as an unicode string.
    """
    if isinstance(path, str):
        path = path.encode("utf-8")  # str -> bytes
    # path = quote(path)
    # urlunsplit: Combine the elements of a tuple as returned by urlsplit() into a complete URL as a string.
    # The parts argument can be any five-item iterable. This may result in a slightly different,
    # but equivalent URL, if the URL that was parsed originally had unnecessary delimiters
    # (for example, a ? with an empty query; the RFC states that these are equivalent).
    # NOTE: urlunsplit expects 5 args of type bytes

    # In [52]: uri = b'/etc/fstab'
    #
    # In [53]: urlunsplit((b'file', b'', uri, b'', b''))
    # Out[53]: b'file:///etc/fstab'

    return urlunsplit((b"file", b"", path, b"", b""))


def uri_to_path(uri: Union[str, bytes]) -> str:
    """
    Convert an URI to a OS specific path.
    Returns a bytestring, since the file path can contain chars with other
    encoding than UTF-8.
    If we had returned these paths as unicode strings, you wouldn't be able to
    look up the matching dir or file on your file system because the exact path
    would be lost by ignoring its encoding.
    """
    # convert str to byte
    if isinstance(uri, str):
        uri = uri.encode("utf-8")

        # logger.debug('URI:')
        # logger.debug(uri)
        # In [6]: urlsplit(uri)
        # Out[6]: SplitResultBytes(scheme=b'file', netloc=b'', path=b'/etc/fstab', query=b'', fragment=b'')
        # In [7]: urlsplit(uri).path
        # Out[7]: b'/etc/fstab'
    _path = urlsplit(uri).path

    if isinstance(_path, bytes):
        _path = _path.decode("utf-8")

    return unquote(_path)


# SOURCE:
# https://github.com/araczkowski/mopidy-rstation/blob/master/mopidy_rstation/file/mpath.py
def _find_worker(relative, follow, done, work, results, errors):  # pragma: no cover
    """Worker thread for collecting stat() results.
    :param str relative: directory to make results relative to
    :param bool follow: if symlinks should be followed
    :param threading.Event done: event indicating that all work has been done
    :param queue.Queue work: queue of paths to process
    :param dict results: shared dictionary for storing all the stat() results
    :param dict errors: shared dictionary for storing any per path errors
    """
    while not done.is_set():
        try:
            entry, parents = work.get(block=False)
        except queue.Empty:
            continue

        if relative:
            path = os.path.relpath(entry, relative)
        else:
            path = entry

        try:
            if follow:
                st = os.stat(entry)
            else:
                st = os.lstat(entry)

            if (st.st_dev, st.st_ino) in parents:
                errors[path] = exceptions.FindError("Sym/hardlink loop found.")
                continue

            parents = parents + [(st.st_dev, st.st_ino)]
            if stat.S_ISDIR(st.st_mode):
                for e in os.listdir(entry):
                    work.put((os.path.join(entry, e), parents))
            elif stat.S_ISREG(st.st_mode):
                results[path] = st
            elif stat.S_ISLNK(st.st_mode):
                errors[path] = exceptions.FindError("Not following symlinks.")
            else:
                errors[path] = exceptions.FindError("Not a file or directory.")

        except OSError as e:
            errors[path] = exceptions.FindError(
                encoding.locale_decode(e.strerror), e.errno
            )
        finally:
            work.task_done()


def _find(root, thread_count=10, relative=False, follow=False):  # pragma: no cover
    """Threaded find implementation that provides stat results for files.
    Tries to protect against sym/hardlink loops by keeping an eye on parent
    (st_dev, st_ino) pairs.
    :param str root: root directory to search from, may not be a file
    :param int thread_count: number of workers to use, mainly useful to
        mitigate network lag when scanning on NFS etc.
    :param bool relative: if results should be relative to root or absolute
    :param bool follow: if symlinks should be followed
    """
    threads = []
    results = {}
    errors = {}
    done = threading.Event()
    work = queue.Queue()
    work.put((os.path.abspath(root), []))

    if not relative:
        root = None

    args = (root, follow, done, work, results, errors)
    for i in range(thread_count):
        t = threading.Thread(target=_find_worker, args=args)
        t.daemon = True
        t.start()
        threads.append(t)

    work.join()
    done.set()
    for t in threads:
        t.join()
    return results, errors


def find_mtimes(root, follow=False):  # pragma: no cover
    results, errors = _find(root, relative=False, follow=follow)
    # return the mtimes as integer milliseconds
    mtimes = {f: int(st.st_mtime * 1000) for f, st in list(results.items())}
    return mtimes, errors


def is_path_inside_base_dir(path, base_path):  # pragma: no cover
    if not isinstance(path, bytes):
        raise ValueError("path is not a bytestring")
    if not isinstance(base_path, bytes):
        raise ValueError("base_path is not a bytestring")

    if path.endswith(os.sep):
        raise ValueError("Path %s cannot end with a path separator" % path)
    # Expand symlinks
    real_base_path = os.path.realpath(base_path)
    real_path = os.path.realpath(path)

    if os.path.isfile(path):
        # Use dir of file for prefix comparision, so we don't accept
        # /tmp/foo.m3u as being inside /tmp/foo, simply because they have a
        # common prefix, /tmp/foo, which matches the base path, /tmp/foo.
        real_path = os.path.dirname(real_path)

    # Check if dir of file is the base path or a subdir
    common_prefix = os.path.commonprefix([real_base_path, real_path])
    return common_prefix == real_base_path


########################################################################################################
# Check whether a path is valid in Python without creating a file at the path's target
# INFO: https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta
########################################################################################################

# Sadly, Python fails to provide the following magic number for us.
ERROR_INVALID_NAME = 123
# Windows-specific error code indicating an invalid pathname.
# See Also
# ----------
# https://docs.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-
#     Official listing of all such codes.


def is_pathname_valid(pathname: str) -> bool:
    """
    `True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.
    """
    # If this pathname is either not a string or is but is empty, this pathname
    # is invalid.
    try:
        if not isinstance(pathname, str) or not pathname:
            return False

        # Strip this pathname's Windows-specific drive specifier (e.g., `C:\`)
        # if any. Since Windows prohibits path components from containing `:`
        # characters, failing to strip this `:`-suffixed prefix would
        # erroneously invalidate all valid absolute Windows pathnames.
        _, pathname = os.path.splitdrive(pathname)

        # Directory guaranteed to exist. If the current OS is Windows, this is
        # the drive to which Windows was installed (e.g., the "%HOMEDRIVE%"
        # environment variable); else, the typical root directory.
        root_dirname = (
            os.environ.get("HOMEDRIVE", "C:")
            if sys.platform == "win32"
            else os.path.sep
        )
        assert os.path.isdir(root_dirname)  # ...Murphy and her ironclad Law

        # Append a path separator to this directory if needed.
        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        # Test whether each path component split from this pathname is valid or
        # not, ignoring non-existent and non-readable path components.
        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            # If an OS-specific exception is raised, its error code
            # indicates whether this pathname is valid or not. Unless this
            # is the case, this exception implies an ignorable kernel or
            # filesystem complaint (e.g., path not found or inaccessible).
            #
            # Only the following exceptions indicate invalid pathnames:
            #
            # * Instances of the Windows-specific "WindowsError" class
            #   defining the "winerror" attribute whose value is
            #   "ERROR_INVALID_NAME". Under Windows, "winerror" is more
            #   fine-grained and hence useful than the generic "errno"
            #   attribute. When a too-long pathname is passed, for example,
            #   "errno" is "ENOENT" (i.e., no such file or directory) rather
            #   than "ENAMETOOLONG" (i.e., file name too long).
            # * Instances of the cross-platform "OSError" class defining the
            #   generic "errno" attribute whose value is either:
            #   * Under most POSIX-compatible OSes, "ENAMETOOLONG".
            #   * Under some edge-case OSes (e.g., SunOS, *BSD), "ERANGE".
            except OSError as exc:
                if hasattr(exc, "winerror"):
                    if exc.winerror == ERROR_INVALID_NAME:  # pylint: disable=no-member
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    # If a "TypeError" exception was raised, it almost certainly has the
    # error message "embedded NUL character" indicating an invalid pathname.
    except TypeError as exc:
        return False
    # If no exception was raised, all path components and hence this
    # pathname itself are valid. (Praise be to the curmudgeonly python.)
    else:
        return True
    # If any other exception was raised, this is an unrelated fatal issue
    # (e.g., a bug). Permit this exception to unwind the call stack.
    #
    # Did we mention this should be shipped with Python already?


def is_path_creatable(pathname: str) -> bool:
    """
    `True` if the current user has sufficient permissions to create the passed
    pathname; `False` otherwise.
    """
    # Parent directory of the passed path. If empty, we substitute the current
    # working directory (CWD) instead.
    dirname = os.path.dirname(pathname) or os.getcwd()
    return os.access(dirname, os.W_OK)


def is_path_exists_or_creatable(pathname: str) -> bool:
    """
    `True` if the passed pathname is a valid pathname for the current OS _and_
    either currently exists or is hypothetically creatable; `False` otherwise.

    This function is guaranteed to _never_ raise exceptions.
    """
    try:
        # To prevent "os" module calls from raising undesirable exceptions on
        # invalid pathnames, is_pathname_valid() is explicitly called first.
        return is_pathname_valid(pathname) and (
            os.path.exists(pathname) or is_path_creatable(pathname)
        )
    # Report failure on non-fatal filesystem complaints (e.g., connection
    # timeouts, permissions issues) implying this path to be inaccessible. All
    # other exceptions are unrelated fatal issues and should not be caught here.
    except OSError:
        return False


def is_path_sibling_creatable(pathname: str) -> bool:
    """
    `True` if the current user has sufficient permissions to create **siblings**
    (i.e., arbitrary files in the parent directory) of the passed pathname;
    `False` otherwise.
    """
    # Parent directory of the passed path. If empty, we substitute the current
    # working directory (CWD) instead.
    dirname = os.path.dirname(pathname) or os.getcwd()

    try:
        # For safety, explicitly close and hence delete this temporary file
        # immediately after creating it in the passed path's parent directory.
        with tempfile.TemporaryFile(dir=dirname):
            pass
        return True
    # While the exact type of exception raised by the above function depends on
    # the current version of the Python interpreter, all such types subclass the
    # following exception superclass.
    except EnvironmentError:
        return False


def is_path_exists_or_creatable_portable(pathname: str) -> bool:
    """
    `True` if the passed pathname is a valid pathname on the current OS _and_
    either currently exists or is hypothetically creatable in a cross-platform
    manner optimized for POSIX-unfriendly filesystems; `False` otherwise.

    This function is guaranteed to _never_ raise exceptions.
    """
    try:
        # To prevent "os" module calls from raising undesirable exceptions on
        # invalid pathnames, is_pathname_valid() is explicitly called first.
        return is_pathname_valid(pathname) and (
            os.path.exists(pathname) or is_path_sibling_creatable(pathname)
        )
    # Report failure on non-fatal filesystem complaints (e.g., connection
    # timeouts, permissions issues) implying this path to be inaccessible. All
    # other exceptions are unrelated fatal issues and should not be caught here.
    except OSError:
        return False


# Dare we? It's time to test-drive the above tests.

# Since NULL is the only character prohibited in pathnames on UNIX-oriented filesystems, let's leverage that to demonstrate the cold, hard truth - ignoring non-ignorable Windows shenanigans, which frankly bore and anger me in equal measure:

# >>> print('"foo.bar" valid? ' + str(is_pathname_valid('foo.bar')))
# "foo.bar" valid? True
# >>> print('Null byte valid? ' + str(is_pathname_valid('\x00')))
# Null byte valid? False
# >>> print('Long path valid? ' + str(is_pathname_valid('a' * 256)))
# Long path valid? False
# >>> print('"/dev" exists or creatable? ' + str(is_path_exists_or_creatable('/dev')))
# "/dev" exists or creatable? True
# >>> print('"/dev/foo.bar" exists or creatable? ' + str(is_path_exists_or_creatable('/dev/foo.bar')))
# "/dev/foo.bar" exists or creatable? False
# >>> print('Null byte exists or creatable? ' + str(is_path_exists_or_creatable('\x00')))
# Null byte exists or creatable? False

###############################################################################################################

# TODO: Get rid of this function
def uri_is_valid(uri):  # pragma: no cover
    """Checks if the specified URI is usable (of type file://).
    Will also check if the size is valid (> 0).
    Args:
        uri (str): The location to check.
    Return:
        (boolean): True if valid, False otherwise.
    """

    # If we have a byte instead of a strng, decode to str type
    if isinstance(uri, bytes):
        uri = uri.decode("utf-8")

    return is_path_exists_or_creatable(uri)


# FIXME replace with mock usage in tests.
class Mtime(object):  # pragma: no cover
    def __init__(self) -> None:
        self.fake = None

    def __call__(self, path):
        if self.fake is not None:
            return self.fake
        return int(os.stat(path).st_mtime)

    def set_fake_time(self, time):
        self.fake = time

    def undo_fake(self):
        self.fake = None


mtime = Mtime()
