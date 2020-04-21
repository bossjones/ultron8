# Copyright 2015, Adrian Sampson.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

"""Worry-free YAML configuration files.
"""

# import os
# import platform
# from collections import abc, OrderedDict
# import re

# import pkg_resources
# import yaml

# from copy import deepcopy
# from collections import ChainMap

# # from devtest.core import exceptions

# from ultron8.exceptions.config import ConfigError
# from ultron8.exceptions.config import ConfigNotFoundError
# from ultron8.exceptions.config import ConfigValueError
# from ultron8.exceptions.config import ConfigTypeError
# from ultron8.exceptions.config import ConfigTemplateError

from ultron8.config.base import BaseConfiguration

# from ultron8.config.base import ConfigSource
# from ultron8.config.base import RootView
# from ultron8.config.base import Dumper
# from ultron8.config.base import load_yaml
# from ultron8.config.base import restore_yaml_comments
# from ultron8.config.base import config_dirs

# from ultron8.config.base import UNIX_DIR_FALLBACK
# from ultron8.config.base import MAC_DIR
# from ultron8.config.base import WINDOWS_DIR_VAR
# from ultron8.config.base import WINDOWS_DIR_FALLBACK
# from ultron8.config.base import CONFIG_FILENAME
# from ultron8.config.base import DEFAULT_FILENAME
# from ultron8.config.base import ROOT_NAME
# from ultron8.config.base import YAML_TAB_PROBLEM
# from ultron8.config.base import REDACTED_TOMBSTONE
# from ultron8.config.base import UNIX_SYSTEM_DIR


# Base interface. ( NOTE, this is basically the cli config at this moment, need to modify it to work with other types of configs )

############################################################################################################
class Configuration(BaseConfiguration):
    def __init__(self, appname, modname=None, read=True):
        """Create a configuration object by reading the
        automatically-discovered config files for the application for a
        given name. If `modname` is specified, it should be the import
        name of a module whose package will be searched for a default
        config file. (Otherwise, no defaults are used.) Pass `False` for
        `read` to disable automatic reading of all discovered
        configuration files. Use this when creating a configuration
        object at module load time and then call the `read` method
        later.
        """
        super().__init__(appname, modname=modname, read=read)
        self.appname = appname
        self.modname = modname

        self.config_filename = "smart.yaml"
        self.default_filename = "smart_default.yaml"
        self.domain = "user"  # Domain tells the config_dirs command which code path to follow to find the correct location to find configuration files

        self._env_var = "{0}DIR".format(self.appname.upper())

        if read:
            self.read()


class LazyConfig(Configuration):
    """A Configuration at reads files on demand when it is first
    accessed. This is appropriate for using as a global config object at
    the module level.
    """

    def __init__(self, appname, modname=None):
        super().__init__(appname, modname, False)
        self._materialized = False  # Have we read the files yet?
        self._lazy_prefix = []  # Pre-materialization calls to set().
        self._lazy_suffix = []  # Calls to add().

    def read(self, user=True, defaults=True):
        self._materialized = True
        super().read(user, defaults)

    def resolve(self):
        if not self._materialized:
            # Read files and unspool buffers.
            self.read()
            self.sources += self._lazy_suffix
            self.sources[:0] = self._lazy_prefix
        return super().resolve()

    def add(self, value):
        super().add(value)
        if not self._materialized:
            # Buffer additions to end.
            self._lazy_suffix += self.sources
            del self.sources[:]

    def set(self, value):
        super().set(value)
        if not self._materialized:
            # Buffer additions to beginning.
            self._lazy_prefix[:0] = self.sources
            del self.sources[:]

    def clear(self):
        """Remove all sources from this configuration."""
        super().clear()
        self._lazy_suffix = []
        self._lazy_prefix = []
