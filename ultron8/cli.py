from typing import Any
from typing import Tuple

import os
import sys

# import pdb
import click
import pyconfig

from .logging_init import getLogger
from .process import fail

# from click.testing import CliRunner

logger = getLogger(__name__)

stdin, stdout = sys.stdin, sys.stdout


def set_trace():
    """[Use this to set pdb trace for debugging]
    """
    # SOURCE: https://github.com/pallets/click/issues/1121
    # pdb.Pdb(stdin=stdin, stdout=stdout).set_trace()
    pass


# http://click.palletsprojects.com/en/5.x/options/
# http://click.palletsprojects.com/en/5.x/complex/#complex-guide
# http://click.palletsprojects.com/en/5.x/commands/
# https://github.com/pallets/click/blob/master/examples/complex/complex/cli.py


CONTEXT_SETTINGS = dict(auto_envvar_prefix="ULTRON8_CLI")


class Environment(object):
    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_environment = click.make_pass_decorator(Environment, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))


def _info() -> None:
    """Get Info on Ultron"""
    logger.info("Ultron8 is running")


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option("--working-dir", envvar="ULTRON_WORKING_DIR", default="working_dir")
@click.option("--config-dir", envvar="ULTRON_CONFIG_DIR", default=".config")
@click.option("--debug", is_flag=True, envvar="ULTRON_DEBUG")
@click.option("-v", "--verbose", count=True, help="Enables verbose mode.")
@click.pass_context
def cli(ctx, working_dir: str, config_dir: str, debug: bool, verbose: int):
    """
    Ultronctl - Client Side CLI tool to manage an Ultron8 Cluster.
    """
    # SOURCE: http://click.palletsprojects.com/en/7.x/commands/?highlight=__main__
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below
    ctx.ensure_object(dict)

    set_flag("working-dir", working_dir)
    set_flag("config-dir", config_dir)
    set_flag("debug", debug)
    set_flag("verbose", verbose)

    ctx.obj["working_dir"] = working_dir
    ctx.obj["config_dir"] = config_dir
    ctx.obj["debug"] = debug
    ctx.obj["verbose"] = verbose

    # pass


# SOURCE: https://kite.com/blog/python/python-command-line-click-tutorial/


@cli.command()
@click.pass_context
def dummy(ctx):
    """
    Dummy command, doesn't do anything.
    """
    if get_flag("debug"):
        click.echo("Debug mode initiated")
        set_trace()

    if get_flag("debug"):
        click.echo("[DUMP ctx]: ")
        for k, v in ctx.obj.items():
            click.echo(f"  {k} -> {v}")

    click.echo("Dummy command, doesn't do anything.")


@cli.command()
@click.option("--fact", multiple=True, help="Set a fact, like --fact=color:blue.")
@click.pass_context
def info(ctx, fact: Tuple[str]):
    """Get info on running Ultron8 process."""
    if get_flag("debug"):
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("info subcommand called from cli")
    set_fact_flags(fact)
    _info()


# @cli.command()
# @click.option('--clean-assets', is_flag=True, help='Also remove assets.')
# def clean(clean_assets: bool):
#     """Remove rendered files and downloaded assets."""
#     logger.debug('clean subcommand called from cli')
#     set_flag('clean-assets', clean_assets)
#     commands.clean()


# @cli.command()
# @click.option('--clean-assets', is_flag=True, help='Reaquire assets.')
# @click.option('--asset-set', default='default', help='Specify the asset set to build with.')
# @click.option('--fact', multiple=True, help='Set a fact, like --fact=color:blue.')
# def build(clean_assets: bool, asset_set: str, fact: Tuple[str]):
#     """Build images."""
#     logger.debug('build subcommand called from cli')
#     set_flag('asset-set', asset_set)
#     set_flag('clean-assets', clean_assets)
#     set_fact_flags(fact)
#     # FIXME: Should we auto-clean assets if the assetset changes?
#     commands.clean()
#     commands.acquire()
#     commands.render()
#     commands.build()


# @cli.command()
# @click.option('--asset-set', default='default', help='Specify the asset set to acquire.')
# @click.option('--fact', multiple=True, help='Set a fact, like --fact=color:blue.')
# def acquire(asset_set: str, fact: Tuple[str]):
#     """Acquire assets."""
#     logger.debug('acquire subcommand called from cli')
#     set_flag('asset-set', asset_set)
#     set_fact_flags(fact)

#     # Since the user explicitly called "acquire", make sure they get fresh assets
#     # by cleaning the assets dir first.
#     set_flag('clean-assets', True)
#     commands.clean()

#     commands.acquire()

# @cli.command()
# @click.option('--asset-set', default='default', help='Specify the asset set to acquire.')
# @click.option('--fact', multiple=True, help='Set a fact, like --fact=color:blue.')
# def acquire(asset_set: str, fact: Tuple[str]):
#     """Acquire assets."""
#     logger.debug('acquire subcommand called from cli')
#     set_flag('asset-set', asset_set)
#     set_fact_flags(fact)

#     # Since the user explicitly called "acquire", make sure they get fresh assets
#     # by cleaning the assets dir first.
#     set_flag('clean-assets', True)
#     commands.clean()

#     commands.acquire()


def set_flag(flag: str, value: Any) -> None:
    """Store a CLI flag in the config as "cli.flags.FLAG"."""
    pyconfig.set(f"cli.flags.{flag}", value)


def get_flag(flag: str, default: Any = None) -> Any:
    """Get a CLI flag from the config."""
    return pyconfig.get(f"cli.flags.{flag}", default)


def set_fact_flags(flag_args: Tuple[str]) -> None:
    """Take "--fact" flags from the CLI and store them in the config as a dict."""
    facts = {}

    for arg in flag_args:
        if ":" not in arg:
            logger.critical('Arguments to "--fact" must be colon seperated.')
            logger.critical('Like: "ultronctl --fact=temperature:hot')
            fail()
        fact, value = arg.split(":", 1)
        logger.debug(f'Setting fact from cli: "{fact}" -> "{value}"')
        facts[fact] = value

    set_flag("fact", facts)


# import logging
# import random
# import string

# import requests

# from ultron8.api import settings

# from typing import Dict

# logger = logging.getLogger(__name__)


# def random_lower_string() -> str:
#     return "".join(random.choices(string.ascii_lowercase, k=32))


# def get_server_api() -> str:
#     server_name = f"http://{settings.SERVER_NAME}"
#     logger.debug("server_name: '%s'", server_name)
#     return server_name


# def get_superuser_token_headers() -> Dict[str, str]:
#     server_api = get_server_api()
#     login_data = {
#         "username": settings.FIRST_SUPERUSER,
#         "password": settings.FIRST_SUPERUSER_PASSWORD,
#     }
#     r = requests.post(
#         f"{server_api}{settings.API_V1_STR}/login/access-token", data=login_data
#     )
#     tokens = r.json()
#     a_token = tokens["access_token"]
#     headers = {"Authorization": f"Bearer {a_token}"}
#     # superuser_token_headers = headers
#     return headers

# if __name__ == '__main__':
#     cli()

# if __name__ == '__main__':
#     print(sys.argv[1:])
#     runner = CliRunner()
#     print(runner.invoke(cli))
if __name__ == "__main__":
    # print(sys.argv[1:])
    # runner = CliRunner()
    # print(runner.invoke(cli, args=sys.argv[1:]))
    cli(sys.argv[1:])
