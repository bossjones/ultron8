import click
import pyconfig
from typing import Any, Tuple
from . import commands
from .logging import getLogger
from .process import fail

logger = getLogger(__name__)

# http://click.palletsprojects.com/en/5.x/options/
# http://click.palletsprojects.com/en/5.x/complex/#complex-guide
# http://click.palletsprojects.com/en/5.x/commands/


@click.group()
@click.option("--working-dir", envvar="ULTRON_WORKING_DIR", default="working_dir")
@click.option("--config-dir", envvar="ULTRON_CONFIG_DIR", default="config")
@click.option("--debug", is_flag=True, envvar="ULTRON_DEBUG")
@click.pass_context
def cli(ctx, working_dir: str, config_dir: str, debug: bool):
    """
    Ultronctl - Client Side CLI tool to manage an Ultron8 Cluster.
    """
    click.echo(f"debug={debug}")

    set_flag("working-dir", working_dir)
    set_flag("config-dir", config_dir)
    set_flag("debug", debug)
    # pass


@cli.command()
def dummy():
    """
    Dummy command, doesn't do anything.
    """

    click.echo("Dummy command, doesn't do anything.")


@cli.command()
@click.option("--fact", multiple=True, help="Set a fact, like --fact=color:blue.")
def info(fact: Tuple[str]):
    """Get info on running Ultron8 process."""
    logger.debug("info subcommand called from cli")
    set_fact_flags(fact)
    commands.info()


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
