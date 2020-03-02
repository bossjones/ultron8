from __future__ import absolute_import
from __future__ import unicode_literals

import os

import pyconfig

from typing import Any
from typing import Tuple
from typing import List

ULTRON_BASE_CONFIG_DIRECTORY = "~/.ultron8"
ULTRON_CONFIG_DIRECTORY = os.path.abspath(
    os.path.expanduser(ULTRON_BASE_CONFIG_DIRECTORY)
)
ULTRON_CONFIG_PATH = os.path.abspath(
    os.path.join(ULTRON_CONFIG_DIRECTORY, "config.json")
)
ULTRON_CLUSTERS_PATH = os.path.abspath(
    os.path.join(ULTRON_CONFIG_DIRECTORY, "clusters")
)
ULTRON_CACHE_PATH = os.path.abspath(os.path.join(ULTRON_CONFIG_DIRECTORY, "cache"))
ULTRON_WORKSPACE_PATH = os.path.abspath(
    os.path.join(ULTRON_CONFIG_DIRECTORY, "workspace")
)
ULTRON_LIBS_PATH = os.path.abspath(os.path.join(ULTRON_CONFIG_DIRECTORY, "libs"))
ULTRON_TEMPLATES_PATH = os.path.abspath(
    os.path.join(ULTRON_WORKSPACE_PATH, "templates")
)


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
