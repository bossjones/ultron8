import shutil
import re
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

# TODO: Mock or monkeypatch CliWorkspace ?
# TODO: Mock or monkeypatch prep_default_config ?
# TODO: Mock or monkeypatch UltronAPI ?


# TODO: Capture data from print() statements and validate them https://docs.pytest.org/en/latest/capture.html


# SOURCE: https://github.com/elastic/tedi/blob/cdb772b78c5568cc478668692a4e006958c0b9c3/tedi/tests/test_cli.py
# @contextmanager
@pytest.fixture
def cli_runner_isolated(request, monkeypatch):
    fixture_path = fixtures_path / "isolated_config_dir"
    runner = CliRunner()
    with runner.isolated_filesystem() as isolated_dir:
        isolated_base_dir = isolated_dir
        isolated_xdg_config_home_dir = os.path.join(isolated_dir, ".config")
        isolated_ultron_config_dir = os.path.join(
            isolated_xdg_config_home_dir, "ultron8"
        )
        isolated_ultron_config_path = os.path.join(
            isolated_ultron_config_dir, "smart.yaml"
        )

        os.makedirs(isolated_xdg_config_home_dir)
        os.makedirs(isolated_ultron_config_dir)

        request.cls.home = isolated_base_dir
        request.cls.xdg_config_home = isolated_xdg_config_home_dir
        request.cls.ultron_config_dir = isolated_ultron_config_dir
        request.cls.ultron_config_path = isolated_ultron_config_path

        monkeypatch.setenv("HOME", request.cls.home)
        monkeypatch.setenv("XDG_CONFIG_HOME", request.cls.xdg_config_home)
        monkeypatch.setenv("ULTRON8DIR", request.cls.ultron_config_dir)

        # Copy the project fixture into the isolated filesystem dir.
        shutil.copytree(fixture_path, isolated_ultron_config_dir)

        # Monkeypatch a helper method onto the runner to make running commands
        # easier.
        runner.run = lambda command: runner.invoke(cli, command.split())

        # And another for checkout the text output by the command.
        runner.output_of = lambda command: runner.run(command).output
        yield runner, isolated_dir


@pytest.mark.skipif(
    sys.stdout.encoding not in ["UTF-8", "UTF8"],
    reason="Need UTF-8 terminal (not {})".format(sys.stdout.encoding),
)
@pytest.mark.clionly
@pytest.mark.integration
class TestCliUserCmd:
    def test_cli_user_no_args(self, request, monkeypatch) -> None:
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
            result = runner.invoke(cli, ["user"])

            # verify results
            assert result.exit_code == 0
            assert "Usage: cli user [OPTIONS] COMMAND [ARGS]..." in result.output
            assert "User CLI. Used to interact with ultron8 api." in result.output
            assert "Options:" in result.output
            assert "--cluster TEXT  Cluster Name eg 'local'" in result.output
            assert "--help          Show this message and exit." in result.output
            assert "Commands:" in result.output
            assert "create  create user from payload" in result.output
            assert "list    list command for users" in result.output

    def test_cli_user_list(self, request, monkeypatch) -> None:
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
            result = runner.invoke(
                cli, ["user", "--cluster", "local", "list", "--output", "table"]
            )

            print(result)
            # verify results
            assert result.exit_code == 0
            # NOTE: This regex grabs the header
            # (?:ID)\s+\S\s+(?:Full Name)\s+\S\s+(?:Email)\s+\S\s+(?:Is Active)\s+\S\s+(?:Is Superuser)\s+\S\s+
            # (?:1)\s+\S\s+(?:None)\s+\S\s+(?:admin@ultron8.com)\s+\S\s+(?:True)\s+\S\s+(?:True)\s+\S\s+

            # FIXME: need to set window size to correctly get result back from this
            # assert "╔═════╦═══════════╦══════════════════════════════════╦═══════════╦══════════════╗" in result.output
            # assert "║ ID  ║ Full Name ║ Email                            ║ Is Active ║ Is Superuser ║" in result.output
            # assert "╠═════╬═══════════╬══════════════════════════════════╬═══════════╬══════════════╣" in result.output
            # assert "║ 1   ║ None      ║ admin@ultron8.com                ║ True      ║ True         ║" in result.output
            # assert "╠═════╬═══════════╬══════════════════════════════════╬═══════════╬══════════════╣" in result.output

            result_lines = result.output.split("\n")

            find_str = []

            for i in range(0, 10):
                if "║ID║Email║FullName║IsActive║IsSuperuser║" in result_lines[
                    i
                ].replace(" ", ""):
                    find_str.append(result_lines[i])
                if "║1║admin@ultron8.com║None║True║True║" in result_lines[i].replace(
                    " ", ""
                ):
                    find_str.append(result_lines[i])

            # should have found the header and the first tet user.
            assert len(find_str) == 2

    def test_cli_user_list_with_debug_and_json_output(
        self, request, monkeypatch
    ) -> None:
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
            result = runner.invoke(
                cli,
                ["--debug", "user", "--cluster", "local", "list", "--output", "json"],
            )

            # verify results
            assert result.exit_code == 0
