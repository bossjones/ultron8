from typing import Any
from typing import Tuple

import os
import sys

import click

# import pyconfig

from ultron8.logging_init import getLogger

# from ultron8.process import fail
from ultron8.cli import set_trace, get_flag, set_fact_flags

logger = getLogger(__name__)

stdin, stdout = sys.stdin, sys.stdout


def _info() -> None:
    """Get Info on Ultron"""
    logger.info("Ultron8 is running")


@click.command("info", short_help="Get info on running Ultron8 process")
@click.option("--fact", multiple=True, help="Set a fact, like --fact=color:blue.")
@click.pass_context
def cli(ctx, fact: Tuple[str]):
    """Get info on running Ultron8 process."""
    if get_flag("debug"):
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("info subcommand called from cli")
    set_fact_flags(fact)
    _info()
