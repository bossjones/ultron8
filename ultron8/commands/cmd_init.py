from typing import Any
from typing import Tuple

import os
import sys

import click

from ultron8.logging_init import getLogger

from ultron8.cli import set_trace, get_flag, set_fact_flags

logger = getLogger(__name__)

stdin, stdout = sys.stdin, sys.stdout


@click.command("init", short_help="Init cmd to setup workspace etc for ultron8.")
@click.pass_context
def cli(ctx):
    """init cmd to setup workspace etc for ultron8."""
    if get_flag("debug"):
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("init subcommand called from cli")
