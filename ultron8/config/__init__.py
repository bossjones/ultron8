from __future__ import absolute_import
from __future__ import unicode_literals

import os
import sys
import logging
import yaml
import inspect

import pyconfig

from typing import Any
from typing import Tuple
from typing import List

from ultron8.paths import mkdir_if_does_not_exist
from ultron8.process import fail

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


def setup_api_pts():
    pass


def setup_cli_opts():
    # 1. check_folder_structure
    # 2. load_config
    # 3. check_environment_overrides
    pass


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
