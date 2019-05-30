#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Config, yaml based config object using the ruamel python module"""

# pylint: disable=line-too-long
# pylint: disable=W1202
import sys
import codecs
import os
import logging

import ultron8.utils as utils

from ultron8.yaml import yaml, YAMLError, yaml_load, yaml_save

import json as jsonlib

LOGGER = logging.getLogger(__name__)

from ultron8.validation import run_moonbeam_service_schema_validation


class Config(object):
    CONFIG_PATH = "/".join(
        (os.path.expanduser("~"), ".config", "ultron8", "config.yaml")
    )

    DEFAULT_CONFIG = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "default_config.yaml"
    )

    def __init__(self, config_path=None, default_config=None):
        self.profiles = None

        self.profile_names = []

        # Initalize the private vars
        self._config_path = None
        self._default_config = None

        # set the properties at instance creation
        # SOURCE: https://stackoverflow.com/questions/2681243/how-should-i-declare-default-values-for-instance-variables-in-python
        # Correct pattern for setting default values defined by Immutable Class Vars.
        self.config_path = config_path if config_path is not None else self.CONFIG_PATH
        self.default_config = (
            default_config if default_config is not None else self.DEFAULT_CONFIG
        )

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
        utils.mkdir_if_does_not_exist(os.path.dirname(Config.CONFIG_PATH))

    def load(self):
        self.check_folder_structure()
        self.profiles = yaml_load(Config.CONFIG_PATH)

        self.profile_names = []
        for key, _ in self.profiles.items():
            self.profile_names.append(str(key))

    def prep_default_config(self):
        """setup config.yaml defaults."""

        # Step 1. ensure sub directory actually exists
        self.check_folder_structure()

        # Step 2. check if config file exists, if it doesnt, create a default config
        if not os.path.exists(Config.CONFIG_PATH):
            # Step 2a. Load default
            default_config = yaml_load(Config.DEFAULT_CONFIG)

            yaml_save(Config.CONFIG_PATH, default_config)

            print(
                "Default config is set, please don't forget to update your github tokens, webhook tokens, and jenkins configurations appropiately! Location = {}".format(
                    Config.CONFIG_PATH
                )
            )


class MoonbeamServiceConfig(object):
    # FIXME: 10/1/2018 - Put this into regular config, then have MoonbeamServiceConfig update the values after instantiation
    DEFAULT_SERVICE_CONFIG_REPO = (
        "git@git.corp.adobe.com:behance/be-moonbeam-configs.git"
    )

    # FIXME: 10/1/2018 - Put this into regular config, then have MoonbeamServiceConfig update the values after instantiation
    DEFAULT_SERVICE_CONFIG_BRANCH = "master"

    # FIXME: 10/1/2018 - Put this into regular config, then have MoonbeamServiceConfig update the values after instantiation
    DEFAULT_SERVICE_CONFIG_PATH = "/".join(
        (os.path.expanduser("~"), ".share", "ultron8", "be-moonbeam-configs")
    )

    def __init__(self, git_repo=None, git_branch=None, service_config_path=None):
        self._config = None
        self.service_definition = None
        self.service_names = []

        self._git_repo = None
        self._git_branch = None
        self._service_config_path = None

        # set the properties at instance creation
        # SOURCE: https://stackoverflow.com/questions/2681243/how-should-i-declare-default-values-for-instance-variables-in-python
        # Correct pattern for setting default values defined by Immutable Class Vars.
        self.git_repo = (
            git_repo if git_repo is not None else self.DEFAULT_SERVICE_CONFIG_REPO
        )
        self.git_branch = (
            git_branch if git_branch is not None else self.DEFAULT_SERVICE_CONFIG_BRANCH
        )
        self.service_config_path = (
            service_config_path
            if service_config_path is not None
            else self.DEFAULT_SERVICE_CONFIG_PATH
        )

        # FIXME: 10/3/2018 - This needs to be enabled for things to work!!!!
        # self.init_merge_moonbeam_service_config_data()

    @property
    def git_repo(self):
        return self._git_repo

    @git_repo.setter
    def git_repo(self, value):
        print("setting: self._git_repo = {}".format(value))
        self._git_repo = value

    @git_repo.deleter
    def git_repo(self):
        print("deleting: self._git_repo")
        del self._git_repo

    @property
    def git_branch(self):
        return self._git_branch

    @git_branch.setter
    def git_branch(self, value):
        print("setting: self._git_branch = {}".format(value))
        self._git_branch = value

    @git_branch.deleter
    def git_branch(self):
        print("deleting: self._git_branch")
        del self._git_branch

    @property
    def service_config_path(self):
        return self._service_config_path

    @service_config_path.setter
    def service_config_path(self, value):
        print("setting: self._service_config_path = {}".format(value))
        self._service_config_path = value

    @service_config_path.deleter
    def service_config_path(self):
        print("deleting: self._service_config_path")
        del self._service_config_path

    def check_folder_structure(self):
        utils.mkdir_p(os.path.abspath(os.path.join(self.service_config_path, os.pardir)))

    # NOTE: Validation rules that involve multiple fields can be implemented as custom validators. It's recommended to use All() to do a two-pass validation - the first pass checking the basic structure of the data, and only after that, the second pass applying your cross-field validator:
    def validate(self):
        self.service_definition = run_moonbeam_service_schema_validation(
            self.service_definition
        )
        return self.service_definition

    # def _get_clone(self, git_repo, dest, sha="master"):
    #     utils.git_clone(git_repo, dest, sha=sha)

    def prep_default_config(self):
        """setup config.yaml defaults."""

        # Step 1. ensure sub directory actually exists
        self.check_folder_structure()

        utils.git_clone(self.git_repo, self.service_config_path, sha=self.git_branch)

    def load_config(self):
        self._config = Config()
        self._config.load()

    def init_merge_moonbeam_service_config_data(self):
        # If config hasn't been loaded into memory first, do this.
        if not self._config:
            self.load_config()

        # If config value exists
        if self._config.profiles["moonbeam_service_config"]:

            # git_repo key exists
            if self._config.profiles["moonbeam_service_config"]["git_repo"]:
                self._git_repo = self._config.profiles["moonbeam_service_config"][
                    "git_repo"
                ]

            # git_branch key exists
            if self._config.profiles["moonbeam_service_config"]["git_branch"]:
                self._git_branch = self._config.profiles["moonbeam_service_config"][
                    "git_branch"
                ]

            # service_config_path key exists
            if self._config.profiles["moonbeam_service_config"]["service_config_path"]:
                self._service_config_path = os.path.expanduser(
                    self._config.profiles["moonbeam_service_config"][
                        "service_config_path"
                    ]
                )

        else:

            self._git_repo = MoonbeamServiceConfig.DEFAULT_SERVICE_CONFIG_REPO
            self._service_config_path = (
                MoonbeamServiceConfig.DEFAULT_SERVICE_CONFIG_PATH
            )
            self._git_branch = MoonbeamServiceConfig.DEFAULT_SERVICE_CONFIG_BRANCH

    # MoonbeamServiceConfig.DEFAULT_SERVICE_CONFIG_REPO,
    # MoonbeamServiceConfig.DEFAULT_SERVICE_CONFIG_PATH,
    # sha=MoonbeamServiceConfig.DEFAULT_SERVICE_CONFIG_BRANCH,

    def load_service(self, service_name, version):
        self.check_folder_structure()

        # Step 2. check if it is a git scm repo

        if not os.path.exists(self.service_config_path):
            # no folder & no git
            # CLONE
            utils.git_clone(self.git_repo, self.service_config_path, sha=self.git_branch)
        else:
            # check if it's actually a git repo
            if utils.scm(self.service_config_path) != "git":
                # nuke it
                # clone again
                utils.remove(self.service_config_path)
                utils.git_clone(self.git_repo, self.service_config_path, sha=self.git_branch)

        # FIXME: This needs to be a runtime flag
        utils.git_pull_rebase(self.git_repo, self.service_config_path, sha=self.git_branch)
        fname = "{}.yaml".format(service_name)
        self.service_definition = yaml_load(
            os.path.join(
                MoonbeamServiceConfig.DEFAULT_SERVICE_CONFIG_PATH, version, fname
            ),
            ordered=True,
        )
        self.service_names.append(service_name)

    def dump(self):
        return yaml.dump(self.service_definition)

    # def as_json(self):
    #     """Return the json data for this object.

    #     This is equivalent to calling::

    #         json.dumps(obj.as_dict())

    #     :returns: this object's attributes as a JSON string
    #     :rtype: str
    #     """
    #     return jsonlib.dumps(self.service_definition, default=json_default)

    def as_jsons(self):
        """print to stdout in json form."""
        print(jsonlib.dumps(self.service_definition, indent=4))

    def update_with_secrets(self, profile):
        if not self._config:
            self.load_config()

        # Now override it
        self.service_definition["payload"][0]["jenkins_build_configurations"][0][
            "password"
        ] = self._config.profiles[profile]["jenkins_password"]
        self.service_definition["payload"][0]["services"][0]["repository"][
            "github_webhook_secrets"
        ] = [
            {
                "webhook_type": "pull_request",
                "token": self._config.profiles[profile]["webhook_token"],
            },
            {
                "webhook_type": "comment",
                "token": self._config.profiles[profile]["webhook_token"],
            },
            {
                "webhook_type": "status",
                "token": self._config.profiles[profile]["webhook_token"],
            },
        ]


if __name__ == "__main__":
    import logging
    from ultron8.loggers import setup_logger
    from ultron8.config import Config, MoonbeamServiceConfig
    from ultron8.yaml import yaml
    import json as jsonlib

    setup_logger()

    # load moonbeam service config object
    m_cfg = MoonbeamServiceConfig()
    m_cfg.load_service("flask-ethos-test", "v2")
    print(m_cfg)

    # Test json conversion
    # data_json = m_cfg.as_json()

    # Test json conversion
    m_cfg.as_jsons()

    m_cfg.validate()

    # Repopulate payload with secret values ( instead of 'REDACTED' )
    m_cfg.update_with_secrets("moonbeam-ethos-dev")

    # print(m_cfg.as_json())
