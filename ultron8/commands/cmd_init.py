from typing import Any
from typing import Tuple

import os
import sys

import click

from ultron8.logging_init import getLogger

from ultron8.cli import set_trace, set_fact_flags
from ultron8.config import do_get_flag, do_set_flag

logger = getLogger(__name__)

stdin, stdout = sys.stdin, sys.stdout


@click.group("init", short_help="Init cmd to setup workspace etc for ultron8.")
@click.pass_context
def cli(ctx):
    """init cmd to setup workspace etc for ultron8."""
    if do_get_flag("cli.flags.debug"):
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("init subcommand called from cli")

    ctx.obj["workspace"].setup()
