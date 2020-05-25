import sys

from typing import Tuple

import click

# from ultron8.process import fail
from ultron8.cli import set_fact_flags, set_trace
from ultron8.config import do_get_flag, do_set_flag
from ultron8.logging_init import getLogger

# import pyconfig


logger = getLogger(__name__)

stdin, stdout = sys.stdin, sys.stdout


def _info() -> None:
    """Get Info on Ultron"""
    logger.info("Ultron8 is running")


@click.group("info", short_help="Get info on running Ultron8 process")
@click.option("--fact", multiple=True, help="Set a fact, like --fact=color:blue.")
@click.pass_context
def cli(ctx, fact: Tuple[str]):
    """Get info on running Ultron8 process."""
    if ctx.obj["debug"]:
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("info subcommand called from cli")
    set_fact_flags(fact)
    _info()
