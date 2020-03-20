import shutil
from contextlib import contextmanager
from uuid import uuid4

import pyconfig
from click.testing import CliRunner

from tests.conftest import fixtures_path
from ultron8.cli import cli
from ultron8.cli import get_flag
from ultron8.cli import set_fact_flags
from ultron8.cli import set_flag

# from ultron8.paths import Paths

# from .conftest import fixtures_path

from typing import Iterator

# paths = Paths()


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


# def test_acquire_command_acquires_assets_specified_by_asset_set_flag():
#     with project_runner() as runner:
#         assert command_acquires_asset(runner, 'acquire --asset-set=special', 'special.tar.gz')


# def test_set_flag_assigns_facts_in_config():
#     set_flag('explode', False)
#     assert pyconfig.get('cli.flags.explode') is False


# def test_get_flag_return_cli_flags():
#     pyconfig.set('cli.flags.fly', True)
#     assert get_flag('fly') is True


# def test_get_flag_can_return_a_default():
#     assert get_flag('no-bananas', 'have-a-peanut') == 'have-a-peanut'


# def test_set_fact_flags_assigns_facts_in_config():
#     args = (
#         'key:minor',
#         'tempo:adagio',
#         'time_signature:3:4'  # <- Extra colon. Will it work?
#     )
#     set_fact_flags(args)
#     assert get_flag('fact')['key'] == 'minor'
#     assert get_flag('fact')['tempo'] == 'adagio'
#     assert get_flag('fact')['time_signature'] == '3:4'
