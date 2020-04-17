from __future__ import absolute_import
from __future__ import unicode_literals

import os
import sys
import logging
import yaml
import inspect

from copy import deepcopy
from collections import ChainMap

import pyconfig

from typing import Any
from typing import Tuple
from typing import List

from ultron8.paths import mkdir_if_does_not_exist
from ultron8.process import fail

from ultron8.config import smart

logger = logging.getLogger(__name__)


class ConfigError(Exception):
    """Generic exception class for errors with config validation"""

    pass


# SOURCE: https://kite.com/blog/python/python-command-line-click-tutorial/
def do_set_flag(flag: str, value: Any) -> None:
    """Store config values in global singleton config."""
    pyconfig.set(f"{flag}", value)


def do_get_flag(flag: str, default: Any = None) -> Any:
    """Get config values in global singleton config"""
    return pyconfig.get(f"{flag}", default)


def do_set_multi_flag(data: List[Tuple]) -> None:
    """Multi - Store a CLI flag in the config as "FLAG"."""
    for d in data:
        pyconfig.set(f"{d[0]}", d[1])


# TODO: Allow us to override this value purely for testing purposes 2/25/2018
def get_config_dir_base_path(override=None):
    # source: home-assistant
    """
    Single directory where user-specific configuration files should be written
    EXAMPLE: $HOME or /opt/ultron8
    :rtype: str
    """

    callers_frame = inspect.currentframe().f_back
    logger.debug(
        "This function was called from the file: {}".format(
            callers_frame.f_code.co_filename
        )
    )

    # First try environment var
    if os.environ.get("ULTRON_CLI_BASE_PATH"):
        config_home = os.environ.get("ULTRON_CLI_BASE_PATH")
        logger.debug(
            "Ran {}| config_home={}".format(sys._getframe().f_code.co_name, config_home)
        )
        return config_home

    # Force location to value provided by kwarg override
    if override is not None:
        config_home = override
        logger.debug(
            "Ran {}| config_home={}".format(sys._getframe().f_code.co_name, config_home)
        )
        return config_home

    config_home = os.path.expanduser("~/")
    # NOTE: Automatically get function name
    logger.debug(
        "Ran {}| config_home={}".format(sys._getframe().f_code.co_name, config_home)
    )
    return config_home


def _set_config_file(override=None):
    config_home = get_config_dir_base_path(override)
    config_file = os.path.join(config_home, ".ultron8", "cli.yml")
    do_set_flag("config_file", os.path.abspath(config_file))
    clusters_path = os.path.join(pyconfig.get("config_file"), "clusters")
    cache_path = os.path.join(pyconfig.get("config_file"), "cache")
    workspace_path = os.path.join(pyconfig.get("config_file"), "workspace")
    templates_path = os.path.join(workspace_path, "templates")
    do_set_flag("clusters_path", os.path.abspath(clusters_path))
    do_set_flag("cache_path", os.path.abspath(cache_path))
    do_set_flag("workspace_path", os.path.abspath(workspace_path))
    do_set_flag("templates_path", os.path.abspath(templates_path))


def _load_and_set_cli_config_opts():
    # Load the config file and put it into pyconfig
    with open(pyconfig.get("config_file")) as config_file:
        for k, v in yaml.load(config_file).items():
            do_set_flag(k, v)


# def check_folder_structure():
#     config_file = do_get_flag("config_file")
#     mkdir_if_does_not_exist(os.path.dirname(config_file))

_CONFIG = None  # singleton instance.


# NOTE: For testing ChainMaps, look at this https://github.com/python/cpython/blob/master/Lib/test/test_collections.py
class Config(ChainMap):
    """Top-level configuration object.

    A Singleton configuration object.
    A subclass of :py:class:`collections.ChainMap`, it allows chaining other configurations later.
    """

    def __init__(self, *maps):
        self.__dict__["maps"] = list(maps) or [{}]

    def __getattr__(self, name):
        try:
            return self.__getitem__(name)
        # The expression following from must be an exception or None. It will be set as __cause__ on the raised exception.
        # Setting __cause__ also implicitly sets the __suppress_context__ attribute to True, so that using raise new_exc from None
        # effectively replaces the old exception with the new one for display purposes (e.g. converting KeyError to AttributeError), while leaving the old exception available in __context__ for introspection when debugging.
        except KeyError:
            raise AttributeError(
                "Config: No attribute or key {!r}".format(name)
            ) from None

    def __setattr__(self, name, val):
        self.__setitem__(name, val)

    def __delattr__(self, name):
        self.__delitem__(name)

    # Behaves like defaultdict, returning empty ConfigDict by default.
    def __missing__(self, key):
        value = ConfigDict()
        self.__setitem__(key, value)
        return value


class ConfigDict(dict):
    """Configuration Dictionary.

    Provides both attribute style and normal mapping style syntax to access
    mapping values.

    Also features "reaching into" sub-containers using a dot-delimited syntax
    for the key:

        >>> cf = config.get_config()
        >>> print(cf.flags.debug)
        0
        >>> cf["flags.debug"]
        0
    """

    def __init__(self, *args, **kwargs):
        self.__dict__["_depth"] = kwargs.pop("_depth", 0)
        dict.__init__(self, *args, **kwargs)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, dict.__repr__(self))

    def __str__(self):
        getitem = dict.__getitem__
        s = ["{}{{".format(" " * self._depth)]
        sortedkeys = sorted(self.keys())
        for key in sortedkeys:
            val = getitem(self, key)
            s.append("{}{} = {}".format("  " * self._depth, key, val))
        s.append("{}}}".format(" " * self._depth))
        return "\n".join(s)

    def __setitem__(self, name, value):
        d, name = self._get_subtree(name)
        return dict.__setitem__(d, name, value)

    def __getitem__(self, name):
        d, name = self._get_subtree(name)
        return dict.__getitem__(d, name)

    def __delitem__(self, name):
        d, name = self._get_subtree(name)
        return dict.__delitem__(d, name)

    def _get_subtree(self, name):
        d = self
        depth = self.__dict__["_depth"]
        parts = name.split(".")
        for part in parts[:-1]:
            depth += 1
            d = d.setdefault(part, self.__class__(_depth=depth))
        return d, parts[-1]

    __setattr__ = __setitem__
    __delattr__ = __delitem__

    def __getattr__(self, name):
        try:
            return self.__getitem__(name)
        except KeyError:
            raise AttributeError(
                "AttrDict: No attribute or key {!r}".format(name)
            ) from None

    def copy(self):
        return self.__class__(self)

    __copy__ = copy

    # Deep copies get regular dictionaries, not new AttrDict
    def __deepcopy__(self, memo):
        new = dict()
        for key, value in self.items():
            new[key] = deepcopy(value, memo)
        return new


# TODO: Make this take another argument where you can pass in which type of config class you want it to pull back. Then that class will be dynamically called later. Also maybe re-think usage of a global config ? In the future we might need to add threading RLocks etc as well.
def get_config(initdict=None, _filename=None, **kwargs):
    """Get primary configuration.

    Returns a Configuration instance containing configuration parameters. An
    extra dictionary may be merged in with the 'initdict' parameter.  And
    finally, extra options may also be added with keyword parameters.

    There is only one Config object in the program, and this will return it. This is the primary
    interface to obtain it.

    Returns:
        A :class:`Config` instance.
    """
    global _CONFIG
    if _CONFIG is None:
        cf = smart.Configuration("ultron8", "ultron8.config")
        if _filename:
            cf.set_file(_filename)
        if isinstance(initdict, dict):
            cf.add(initdict)
        cf.add(kwargs)
        _CONFIG = Config(cf.flatten(dclass=ConfigDict))
    return _CONFIG


def show_config(cf, _path=None):
    """Print the configuration as a list of paths and the end value.
    """
    path = _path or []
    keys = sorted(cf.keys())
    for key in keys:
        value = cf[key]
        path.append(key)
        if isinstance(value, dict):
            show_config(value, path)
        else:
            print(".".join(path), "=", repr(value))
        path.pop(-1)


def get_package_config(packagename):
    """Add configuration specific to a package.

    Arguments:
        packagename: name of a package. If the package directory contains a file named
                     "config_default.yaml" the content will be loaded.

    Returns:
        New :class:`Config` with added configuration.
    """
    newcf = smart.Configuration("ultron8", packagename)
    cf = get_config()
    return cf.new_child(newcf.flatten(dclass=ConfigDict))


if __name__ == "__main__":
    # Simple test gets and shows config.
    _CONFIG = None
    cf = get_config()
    cf.flags.debug = 1
    cf.flags.verbose = 1
    assert cf.flags.debug == 1
    _CONFIG = None
    cf = get_config(initdict={"initkey": "initvalue"})
    assert cf.get("initkey", "") == "initvalue"
    # import pdb;pdb.set_trace()
    print(cf)
