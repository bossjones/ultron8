from typing import Any
from typing import Tuple

import os
import sys

# import pdb
import click

# import pyconfig

from ultron8.logging_init import getLogger
from ultron8.process import fail

from ultron8.core.workspace import CliWorkspace, prep_default_config
from ultron8.core.files import load_json_file
from ultron8.config.manager import NullConfig, ConfigProxy
from ultron8.config import do_set_flag

logger = getLogger(__name__)

stdin, stdout = sys.stdin, sys.stdout

CONTEXT_SETTINGS = dict(auto_envvar_prefix="ULTRON8_CLI")


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

DEFAULT_CONFIG = """
clusters:
    instances:
        local:
            url: "http://localhost:11267"
            token: ""
"""


# pass_environment = click.make_pass_decorator(Environment, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))


class UltronCLI(click.Group):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode("ascii", "replace")
            mod = __import__("ultron8.commands.cmd_" + name, None, None, ["cli"])
        except ImportError:
            return
        return mod.cli


# @click.group(context_settings=CONTEXT_SETTINGS)
@click.command(cls=UltronCLI, context_settings=CONTEXT_SETTINGS)
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

    do_set_flag("cli.flags.working-dir", working_dir)
    do_set_flag("cli.flags.config-dir", config_dir)
    do_set_flag("cli.flags.debug", debug)
    do_set_flag("cli.flags.verbose", verbose)

    ctx.obj["working_dir"] = working_dir
    ctx.obj["config_dir"] = config_dir
    ctx.obj["debug"] = debug
    ctx.obj["cfg_file"] = prep_default_config()
    ctx.obj["verbose"] = verbose
    ctx.obj["workspace"] = CliWorkspace()
    ctx.obj["configmanager"] = ConfigProxy(load_json_file(ctx.obj["cfg_file"]))


# # SOURCE: https://kite.com/blog/python/python-command-line-click-tutorial/
# def set_flag(flag: str, value: Any) -> None:
#     """Store a CLI flag in the config as "cli.flags.FLAG"."""
#     pyconfig.set(f"cli.flags.{flag}", value)


# def get_flag(flag: str, default: Any = None) -> Any:
#     """Get a CLI flag from the config."""
#     return pyconfig.get(f"cli.flags.{flag}", default)


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

    do_set_flag("fact", facts)


if __name__ == "__main__":
    # print(sys.argv[1:])
    # runner = CliRunner()
    # print(runner.invoke(cli, args=sys.argv[1:]))
    # pylint: disable=no-value-for-parameter
    cli(sys.argv[1:])
