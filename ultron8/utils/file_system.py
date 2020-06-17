"""
File system related utility functions.
"""

import fnmatch
import os
import os.path
import pwd

import six

__all__ = ["get_file_list", "recursive_chown"]


def get_file_list(directory, exclude_patterns=None):
    """
    Recurisvely retrieve a list of files in the provided directory.

    :param directory: Path to directory to retrieve the file list for.
    :type directory: ``str``

    :param exclude_patterns: A list of `fnmatch` compatible patterns of files to exclude from
                             the result.
     :type exclude_patterns: ``list``

    :return: List of files in the provided directory. Each file path is relative
             to the provided directory.
    :rtype: ``list``
    """
    result = []
    if not directory.endswith("/"):
        # Make sure trailing slash is present
        directory = directory + "/"

    def include_file(file_path):
        if not exclude_patterns:
            return True

        for exclude_pattern in exclude_patterns:
            if fnmatch.fnmatch(file_path, exclude_pattern):
                return False

        return True

    for (dirpath, dirnames, filenames) in os.walk(directory):
        base_path = dirpath.replace(directory, "")

        for filename in filenames:
            if base_path:
                file_path = os.path.join(base_path, filename)
            else:
                file_path = filename

            if include_file(file_path=file_path):
                result.append(file_path)

    return result


def recursive_chown(path, uid, gid):
    """
    Recursive version of os.chown.
    """
    if isinstance(uid, six.string_types) or isinstance(gid, six.string_types):
        result = pwd.getpwnam(uid)
        uid = result.pw_uid
        gid = result.pw_gid

    os.chown(path, uid, gid)

    for item in os.listdir(path):
        itempath = os.path.join(path, item)

        if os.path.isfile(itempath):
            os.chown(itempath, uid, gid)
        elif os.path.isdir(itempath):
            os.chown(itempath, uid, gid)
            recursive_chown(itempath, uid, gid)
