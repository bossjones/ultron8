import shutil
import re
import json
import os
import sys
from contextlib import contextmanager
from uuid import uuid4

import pytest
import click
import pprint
from click.testing import CliRunner

from tests.conftest import fixtures_path
from ultron8.cli import cli

from ultron8.config import do_set_flag
from ultron8.config import do_get_flag
from typing import Iterator

from ultron8.core.workspace import CliWorkspace, prep_default_config
from ultron8.core.files import load_json_file
from ultron8.config.manager import NullConfig, ConfigProxy
from ultron8.config import do_set_flag
from ultron8.config import ConfigManager
from ultron8.client import UltronAPI
from tests.utils.filesystem import helper_write_yaml_to_disk
from tests.utils.utils import get_superuser_jwt_request
from ultron8 import config

from ultron8.api.factories.users import _MakeRandomNormalUserFactory
from fastapi.encoders import jsonable_encoder


@pytest.mark.skipif(
    sys.stdout.encoding not in ["UTF-8", "UTF8"],
    reason="Need UTF-8 terminal (not {})".format(sys.stdout.encoding),
)
@pytest.mark.clionly
@pytest.mark.integration
class TestCliWorkspaceCmd:
    def test_cli_workspace_no_args(self, request, monkeypatch) -> None:
        # reset global config singleton
        config._CONFIG = None
        fixture_path = fixtures_path / "isolated_config_dir"
        print(fixture_path)
        runner = CliRunner()
        with runner.isolated_filesystem() as isolated_dir:
            # Populate filesystem folders
            isolated_base_dir = isolated_dir
            isolated_xdg_config_home_dir = os.path.join(isolated_dir, ".config")
            isolated_ultron_config_dir = os.path.join(
                isolated_xdg_config_home_dir, "ultron8"
            )
            isolated_ultron_config_path = os.path.join(
                isolated_ultron_config_dir, "smart.yaml"
            )

            # create base dirs
            os.makedirs(isolated_xdg_config_home_dir)

            # request.cls.home = isolated_base_dir
            # request.cls.xdg_config_home = isolated_xdg_config_home_dir
            # request.cls.ultron_config_dir = isolated_ultron_config_dir
            # request.cls.ultron_config_path = isolated_ultron_config_path

            # monkeypatch env vars to trick intgr tests into running only in isolated file system
            monkeypatch.setenv("HOME", isolated_base_dir)
            monkeypatch.setenv("XDG_CONFIG_HOME", isolated_xdg_config_home_dir)
            monkeypatch.setenv("ULTRON8DIR", isolated_ultron_config_dir)

            # Copy the project fixture into the isolated filesystem dir.
            shutil.copytree(fixture_path, isolated_ultron_config_dir)

            # Monkeypatch a helper method onto the runner to make running commands
            # easier.
            runner.run = lambda command: runner.invoke(cli, command.split())

            # And another for checkout the text output by the command.
            runner.output_of = lambda command: runner.run(command).output

            # Run click test client
            result = runner.invoke(cli, ["workspace"])

            # verify results
            assert result.exit_code == 0

            assert "Usage: cli workspace [OPTIONS] COMMAND [ARGS]..." in result.output
            assert "Interact with workspace for ultron8." in result.output
            assert "Options:" in result.output
            assert "--help  Show this message and exit." in result.output
            assert "Commands:" in result.output
            assert "info  Info on workspace" in result.output
            assert "tree  Tree command for Workspace" in result.output

    def test_cli_workspace_tree(self, request, monkeypatch) -> None:
        # reset global config singleton
        config._CONFIG = None
        fixture_path = fixtures_path / "isolated_config_dir"
        print(fixture_path)
        runner = CliRunner()
        with runner.isolated_filesystem() as isolated_dir:
            # Populate filesystem folders
            isolated_base_dir = isolated_dir
            isolated_xdg_config_home_dir = os.path.join(isolated_dir, ".config")
            isolated_ultron_config_dir = os.path.join(
                isolated_xdg_config_home_dir, "ultron8"
            )
            isolated_ultron_config_path = os.path.join(
                isolated_ultron_config_dir, "smart.yaml"
            )

            # create base dirs
            os.makedirs(isolated_xdg_config_home_dir)

            # request.cls.home = isolated_base_dir
            # request.cls.xdg_config_home = isolated_xdg_config_home_dir
            # request.cls.ultron_config_dir = isolated_ultron_config_dir
            # request.cls.ultron_config_path = isolated_ultron_config_path

            # monkeypatch env vars to trick intgr tests into running only in isolated file system
            monkeypatch.setenv("HOME", isolated_base_dir)
            monkeypatch.setenv("XDG_CONFIG_HOME", isolated_xdg_config_home_dir)
            monkeypatch.setenv("ULTRON8DIR", isolated_ultron_config_dir)

            # Copy the project fixture into the isolated filesystem dir.
            shutil.copytree(fixture_path, isolated_ultron_config_dir)

            # Grab access token
            r = get_superuser_jwt_request()
            tokens = r.json()
            a_token = tokens["access_token"]

            example_data = """
clusters_path: clusters/
cache_path: cache/
workspace_path: workspace/
templates_path: templates/

flags:
    debug: 0
    verbose: 0
    keep: 0
    stderr: 0
    repeat: 1

clusters:
    instances:
        local:
            url: http://localhost:11267
            token: '{}'
    """.format(
                a_token
            )

            # overwrite smart.yaml w/ config that has auth token in it.
            helper_write_yaml_to_disk(example_data, isolated_ultron_config_path)

            # Monkeypatch a helper method onto the runner to make running commands
            # easier.
            runner.run = lambda command: runner.invoke(cli, command.split())

            # And another for checkout the text output by the command.
            runner.output_of = lambda command: runner.run(command).output

            # Run click test client
            result = runner.invoke(cli, ["--debug", "workspace", "tree"])

            print(result)
            # verify results
            assert result.exit_code == 0

            # TODO: Use the capture fixture and test that it looks like this
            # + /Users/malcolm/.config/ultron8
            #     + clusters
            #     + libs
            #     + smart.yaml
            #     + templates
            #     + workspace

    def test_cli_workspace_info(self, request, monkeypatch) -> None:
        # reset global config singleton
        config._CONFIG = None
        fixture_path = fixtures_path / "isolated_config_dir"
        print(fixture_path)
        runner = CliRunner()
        with runner.isolated_filesystem() as isolated_dir:
            # Populate filesystem folders
            isolated_base_dir = isolated_dir
            isolated_xdg_config_home_dir = os.path.join(isolated_dir, ".config")
            isolated_ultron_config_dir = os.path.join(
                isolated_xdg_config_home_dir, "ultron8"
            )
            isolated_ultron_config_path = os.path.join(
                isolated_ultron_config_dir, "smart.yaml"
            )

            # create base dirs
            os.makedirs(isolated_xdg_config_home_dir)

            # request.cls.home = isolated_base_dir
            # request.cls.xdg_config_home = isolated_xdg_config_home_dir
            # request.cls.ultron_config_dir = isolated_ultron_config_dir
            # request.cls.ultron_config_path = isolated_ultron_config_path

            # monkeypatch env vars to trick intgr tests into running only in isolated file system
            monkeypatch.setenv("HOME", isolated_base_dir)
            monkeypatch.setenv("XDG_CONFIG_HOME", isolated_xdg_config_home_dir)
            monkeypatch.setenv("ULTRON8DIR", isolated_ultron_config_dir)

            # Copy the project fixture into the isolated filesystem dir.
            shutil.copytree(fixture_path, isolated_ultron_config_dir)

            # Grab access token
            r = get_superuser_jwt_request()
            tokens = r.json()
            a_token = tokens["access_token"]

            example_data = """
clusters_path: clusters/
cache_path: cache/
workspace_path: workspace/
templates_path: templates/

flags:
    debug: 0
    verbose: 0
    keep: 0
    stderr: 0
    repeat: 1

clusters:
    instances:
        local:
            url: http://localhost:11267
            token: '{}'
    """.format(
                a_token
            )

            # overwrite smart.yaml w/ config that has auth token in it.
            helper_write_yaml_to_disk(example_data, isolated_ultron_config_path)

            # Monkeypatch a helper method onto the runner to make running commands
            # easier.
            runner.run = lambda command: runner.invoke(cli, command.split())

            # And another for checkout the text output by the command.
            runner.output_of = lambda command: runner.run(command).output

            # Run click test client
            result = runner.invoke(cli, ["--debug", "workspace", "info"])

            print(result)
            # verify results
            assert result.exit_code == 0

            # TODO: Use the capture fixture and test that it looks like this
            # + /Users/malcolm/.config/ultron8
            #     + clusters
            #     + libs
            #     + smart.yaml
            #     + templates
            #     + workspace
