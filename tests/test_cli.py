import os
import shutil
from contextlib import contextmanager
from uuid import uuid4

import pytest
import pyconfig
from click.testing import CliRunner

from tests.conftest import fixtures_path
from ultron8.cli import cli

# from ultron8.cli import get_flag
# from ultron8.cli import set_fact_flags
from ultron8.config import do_set_flag
from ultron8.config import do_get_flag

# from ultron8.paths import Paths

# from .conftest import fixtures_path

from typing import Iterator

# paths = Paths()

# TODO: Capture data from print() statements and validate them https://docs.pytest.org/en/latest/capture.html


@contextmanager
def project_runner(fixture: str = "simple") -> Iterator[CliRunner]:
    fixture_path = fixtures_path / fixture
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Copy the project fixture into the isolated filesystem dir.
        shutil.copytree(fixture_path, ".ultron8")

        # Monkeypatch a helper method onto the runner to make running commands
        # easier.
        runner.run = lambda command: runner.invoke(cli, command.split())

        # And another for checkout the text output by the command.
        runner.output_of = lambda command: runner.run(command).output
        yield runner


# @pytest.fixture
# def runner():
#     return CliRunner()


# @pytest.fixture(scope="function")
# def fake_config(mocker):
#     MockConfig = mocker.patch("moonbeam_cli.cli.Config", spec=True)
#     # mock_config_instance = MockConfig()
#     mock_config_instance = MockConfig.return_value
#     mock_config_instance.load.return_value = {
#         "behance_corp_fake": {
#             "api_url": "https://git.corp.adobe.com/api/v3",
#             "organization": "behance",
#             "token": "fake_token",
#             "whitelist": ["behance/not-to-be-copied"],
#         },
#         "behance_pub_fake": {
#             "api_url": "https://api.github.com",
#             "organization": "behance",
#             "token": "fake_token",
#             "whitelist": ["behance/not-to-be-copied"],
#         },
#     }
#     yield fake_config


# def test_cli_no_args(runner):
#     result = runner.invoke(cli.main_group)
#     assert result.exit_code == 0
#     assert not result.exception
#     assert "Usage: main_group [OPTIONS] COMMAND [ARGS]..." in result.output

# def test_cli_no_args():
#     with project_runner() as runner:
#         assert "Usage: main_group [OPTIONS] COMMAND [ARGS]..." in runner.output_of('render --help')

# def test_cli_dummy():
#     with project_runner() as runner:
#         assert "Dummy command, doesn't do anything" in runner.output_of('dummy')

# def test_cli_info():
#     with project_runner() as runner:
#         assert "Usage: ultronctl [OPTIONS] COMMAND [ARGS]..." in runner.output_of('info')


def test_cli_dummp() -> None:
    with project_runner() as runner:
        assert "Dummy command, doesn't do anything." in runner.output_of("dummy")


# def in_file(string, test_file='simple-vanilla/README.md') -> bool:
#     return (string in (paths.build_path_dir / test_file).open().read())


# def assert_command_cleans_path(runner, path, command):
#     """Given a Ultron subcommand name, assert that it cleans up rendered files."""
#     path.mkdir(parents=True, exist_ok=True)
#     canary = path / ('test-canary-%s' % uuid4())
#     canary.touch()
#     assert runner.run(command).exit_code == 0
#     assert canary.exists() is False


# def command_acquires_asset(runner, command, filename):
#     """Check that an asset file was acquired to the assets dir."""
#     assert runner.run(command).exit_code == 0
#     return (paths.assets_path / filename).exists()


# def test_render_command_has_valid_help_text():
#     with project_runner() as runner:
#         assert 'Render' in runner.output_of('render --help')


# def test_clean_command_removes_rendered_files():
#     with project_runner() as runner:
#         assert_command_cleans_path(runner, paths.build_path_dir, 'clean')


# def test_render_command_cleans_build_path():
#     with project_runner() as runner:
#         assert_command_cleans_path(runner, paths.build_path_dir, 'render')


# def test_render_command_accepts_facts_as_cli_flags():
#     with project_runner() as runner:
#         runner.run('render --fact=cow_color:cherry')
#         assert in_file('How now, cherry cow?')


# def test_build_command_accepts_facts_as_cli_flags():
#     with project_runner() as runner:
#         runner.run('build --fact=cow_color:cinnabar')
#         assert in_file('How now, cinnabar cow?')


# def test_clean_command_removes_assets_with_clean_assets_flag():
#     with project_runner() as runner:
#         assert_command_cleans_path(runner, paths.assets_path, 'clean --clean-assets')


# def test_build_command_removes_assets_with_clean_assets_flag():
#     with project_runner() as runner:
#         assert_command_cleans_path(runner, paths.assets_path, 'build --clean-assets')


# def test_acquire_command_acquires_default_assets():
#     with project_runner() as runner:
#         assert command_acquires_asset(runner, 'acquire', 'default.tar.gz')


# def test_acquire_command_does_not_acquire_non_default_assets():
#     with project_runner() as runner:
#         assert not command_acquires_asset(runner, 'acquire', 'special.tar.gz')


# def test_acquire_command_acquires_assets_specified_by_asset_do_set_flag():
#     with project_runner() as runner:
#         assert command_acquires_asset(runner, 'acquire --asset-set=special', 'special.tar.gz')


# def test_do_set_flag_assigns_facts_in_config():
#     do_set_flag('explode', False)
#     assert pyconfig.get('cli.flags.explode') is False


# def test_do_get_flag_return_cli_flags():
#     pyconfig.set('cli.flags.fly', True)
#     assert do_get_flag('fly') is True


# def test_do_get_flag_can_return_a_default():
#     assert do_get_flag('no-bananas', 'have-a-peanut') == 'have-a-peanut'


# def test_set_fact_flags_assigns_facts_in_config():
#     args = (
#         'key:minor',
#         'tempo:adagio',
#         'time_signature:3:4'  # <- Extra colon. Will it work?
#     )
#     set_fact_flags(args)
#     assert do_get_flag('fact')['key'] == 'minor'
#     assert do_get_flag('fact')['tempo'] == 'adagio'
#     assert do_get_flag('fact')['time_signature'] == '3:4'


@pytest.mark.clionly
@pytest.mark.integration
def test_cli_default_no_args(request, monkeypatch) -> None:
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
        result = runner.invoke(cli, ["--help"])

        # verify results
        assert result.exit_code == 0
        # assert (
        #     "Usage: cli user [OPTIONS] COMMAND [ARGS]...\n\n  User CLI. Used to interact with ultron8 api.\n\nOptions:\n  -m, --method [GET|POST|PUT|DELETE]\n  --help                          Show this message and exit.\n"
        #     in result.output
        # )

        # import pdb;pdb.set_trace()
        assert "Usage: cli [OPTIONS] COMMAND [ARGS]..." in result.output
        assert (
            "Ultronctl - Client Side CLI tool to manage an Ultron8 Cluster."
            in result.output
        )
        assert "Options:" in result.output
        assert "--working-dir TEXT" in result.output
        assert "--config-dir TEXT" in result.output
        assert "--debug" in result.output
        assert "-v, --verbose       Enables verbose mode." in result.output
        assert "--help              Show this message and exit." in result.output
        assert "Commands:" in result.output
        assert "cluster    Manage your ultron8 clusters" in result.output
        assert "config     Manage your ultron8 config" in result.output
        assert "dummy      Dummy command, doesn't do anything." in result.output
        assert "info       Get info on running Ultron8 process" in result.output
        assert (
            "init       Init cmd to setup workspace etc for ultron8." in result.output
        )
        assert "login      Login to ultron8 cluster" in result.output
        assert "metrics    Login to ultron8 cluster" in result.output
        assert "node       Manage your ultron8 nodes" in result.output
        assert "user       User CLI. Used to interact with ultron8 api" in result.output
        assert "version    Get version" in result.output
        assert (
            "workspace  All commands dealing with workspace for ultron8"
            in result.output
        )

        # "Usage: cli [OPTIONS] COMMAND [ARGS]...\n\n  Ultronctl - Client Side CLI tool to manage an Ultron8 Cluster.\n\nOptions:\n  --working-dir TEXT\n  --config-dir TEXT\n  --debug\n  -v, --verbose       Enables verbose mode.\n  --help              Show this message and exit.\n\nCommands:\n  cluster    Manage your ultron8 clusters\n  config     Manage your ultron8 config\n  dummy      Dummy command, doesn't do anything.\n  info       Get info on running Ultron8 process\n  init       Init cmd to setup workspace etc for ultron8.\n  login      Login to ultron8 cluster\n  metrics    Login to ultron8 cluster\n  node       Manage your ultron8 nodes\n  user       User CLI. Used to interact with ultron8 api\n  version    Get version\n  workspace  All commands dealing with workspace for ultron8\n"

        # "Ultronctl - Client Side CLI tool to manage an Ultron8 Cluster."

        # "Options:"
        #   --working-dir TEXT
        #   --config-dir TEXT
        #   --debug
        #   -v, --verbose       Enables verbose mode.
        #   --help              Show this message and exit.

        # Commands:
        #   cluster    Manage your ultron8 clusters
        #   config     Manage your ultron8 config
        #   dummy      Dummy command, doesn't do anything.
        #   info       Get info on running Ultron8 process
        #   init       Init cmd to setup workspace etc for ultron8.
        #   login      Login to ultron8 cluster
        #   metrics    Login to ultron8 cluster
        #   node       Manage your ultron8 nodes
        #   user       User CLI. Used to interact with ultron8 api
        #   version    Get version
        #   workspace  All commands dealing with workspace for ultron8
