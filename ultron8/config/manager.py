#!/usr/bin/env python3
"""Config, yaml based config object using the ruamel python module"""
# pylint: disable=line-too-long
# pylint: disable=W1202
import hashlib
import logging
import os

from typing import Dict, Union

from ultron8.config import ConfigError, config_parse, schema
from ultron8.utils import maybe_decode, maybe_encode
from ultron8.yaml import YAMLError, yaml, yaml_load, yaml_save

from ultron8.paths import mkdir_p, mkdir_if_does_not_exist

# import ultron8.utils as utils

log = logging.getLogger(__name__)

# from ultron8.validation import run_moonbeam_service_schema_validation


def hash_digest(content: str) -> str:
    return hashlib.sha1(maybe_encode(content)).hexdigest()


# https://mypy.readthedocs.io/en/stable/dynamic_typing.html
class NullConfig(object):
    def __getattr__(self, name: str) -> "NullConfig":
        return self

    def __call__(self) -> None:
        return None

    def exists(self) -> bool:
        return False


class ConfigProxy(object):
    """A container around configuration fragments"""

    def __init__(self, data: Union[str, Dict[str, str]]) -> None:
        self.__data = data

    # NOTE: https://stackoverflow.com/questions/33837918/type-hints-solve-circular-dependency
    def __getattr__(self, name: str) -> Union["ConfigProxy", NullConfig]:
        if name in self.__data:
            return ConfigProxy(self.__data[name])
        return NullConfig()

    def __call__(self) -> str:
        return self.__data

    def exists(self) -> bool:
        return True


class ManifestFile(object):
    """Manage the manifest file, which tracks name to filename."""

    MANIFEST_FILENAME = "_manifest.yaml"

    def __init__(self, path):
        self.filename = os.path.join(path, self.MANIFEST_FILENAME)

    def create(self):
        if os.path.isfile(self.filename):
            msg = "Refusing to create manifest. File %s exists."
            log.info(msg % self.filename)
            return

        yaml_save(self.filename, {})

    def add(self, name, filename):
        manifest = yaml_load(self.filename)
        manifest[name] = filename
        yaml_save(self.filename, manifest)

    def delete(self, name):
        manifest = yaml_load(self.filename)
        if name not in manifest:
            msg = "Namespace %s does not exist in manifest, cannot delete."
            log.info(msg % name)
            return

        del manifest[name]
        yaml_save(self.filename, manifest)

    def get_file_mapping(self):
        return yaml_load(self.filename)

    def get_file_name(self, name):
        return self.get_file_mapping().get(name)

    def __contains__(self, name):
        return name in self.get_file_mapping()


class ConfigManager(object):
    """Read, load and write configuration."""

    # CONFIG_PATH = "/".join(
    #     (os.path.expanduser("~"), ".config", "ultron8", "config.yaml")
    # )

    # DEFAULT_CONFIG = os.path.join(
    #     os.path.dirname(os.path.abspath(__file__)), "default_config.yaml"
    # )

    def __init__(self, config_path=None, manifest=None):
        self.config_path = config_path
        self.manifest = manifest or ManifestFile(config_path)
        # self.profiles = None

        # self.profile_names = []

        # # Initalize the private vars
        # self._config_path = None
        # self._default_config = None

        # # set the properties at instance creation
        # # SOURCE: https://stackoverflow.com/questions/2681243/how-should-i-declare-default-values-for-instance-variables-in-python
        # # Correct pattern for setting default values defined by Immutable Class Vars.
        # self.config_path = config_path if config_path is not None else self.CONFIG_PATH
        # self.default_config = (
        #     default_config if default_config is not None else self.DEFAULT_CONFIG
        # )

    @property
    def config_path(self):
        return self._config_path

    @config_path.setter
    def config_path(self, value):
        print("setting: self._config_path = {}".format(value))
        self._config_path = value

    @config_path.deleter
    def config_path(self):
        print("deleting: self._config_path")
        del self._config_path

    @property
    def default_config(self):
        return self._default_config

    @default_config.deleter
    def default_config(self):
        print("deleting: self._default_config")
        del self._default_config

    @default_config.setter
    def default_config(self, value):
        print("setting: self._default_config = {}".format(value))
        self._default_config = value

    def check_folder_structure(self):
        mkdir_if_does_not_exist(os.path.dirname(self.config_path))

    def get_config_name_mapping(self):
        seq = self.manifest.get_file_mapping().items()
        return {name: yaml_load(filename) for name, filename in seq}

    def load(self):
        """Return the fully constructed configuration."""
        log.info("Loading full config from %s" % self.config_path)
        name_mapping = self.get_config_name_mapping()
        return config_parse.ConfigContainer.create(name_mapping)

        # self.check_folder_structure()
        # self.profiles = yaml_load(self.config_path)

        # self.profile_names = []
        # for key, _ in self.profiles.items():
        #     self.profile_names.append(str(key))

    # def prep_default_config(self):
    #     """setup config.yaml defaults."""

    #     # Step 1. ensure sub directory actually exists
    #     self.check_folder_structure()

    #     # Step 2. check if config file exists, if it doesnt, create a default config
    #     if not os.path.exists(self.config_path):
    #         # Step 2a. Load default
    #         default_config = yaml_load(Config.DEFAULT_CONFIG)

    #         yaml_save(self.config_path, default_config)

    #         print(
    #             "Default config is set, please don't forget to update your github tokens, webhook tokens, and jenkins configurations appropiately! Location = {}".format(
    #                 self.config_path
    #             )
    #         )


if __name__ == "__main__":
    # import logging

    # # from ultron8.loggers import setup_logger
    # from ultron8.config import manager
    # from ultron8.yaml import yaml
    # import json as jsonlib
    print("manager")
