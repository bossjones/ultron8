from typing import Any
from typing import Tuple

import os
import sys

import click

# import pyconfig

from ultron8.logging_init import getLogger

from ultron8.cli import set_trace
from ultron8.config import do_get_flag

from ultron8 import __version__

logger = getLogger(__name__)

stdin, stdout = sys.stdin, sys.stdout


def _version() -> None:
    """Get version of Ultron"""
    logger.info("f{__version__}")


@click.group("version", short_help="Get version")
@click.pass_context
def cli(ctx):
    """Get version of running Ultron8 process."""
    if do_get_flag("cli.flags.debug"):
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("info subcommand called from cli")
    _version()
