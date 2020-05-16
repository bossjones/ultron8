import shutil
import os
from contextlib import contextmanager
from uuid import uuid4

import pytest
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


@pytest.mark.clionly
@pytest.mark.integration
def test_cli_user_no_args(request, monkeypatch) -> None:
    fixture_path = fixtures_path / "isolated_config_dir"
    print(fixture_path)
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
        # os.makedirs(isolated_ultron_config_dir)

        # request.cls.home = isolated_base_dir
        # request.cls.xdg_config_home = isolated_xdg_config_home_dir
        # request.cls.ultron_config_dir = isolated_ultron_config_dir
        # request.cls.ultron_config_path = isolated_ultron_config_path

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

        result = runner.invoke(cli, ["user"])
        assert result.exit_code == 0
        assert (
            "Usage: cli user [OPTIONS] COMMAND [ARGS]...\n\n  User CLI. Used to interact with ultron8 api.\n\nOptions:\n  -m, --method [GET|POST|PUT|DELETE]\n  --help                          Show this message and exit.\n"
            in result.output
        )
