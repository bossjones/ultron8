import os
import sys

from typing import Any, Tuple

import click

from ultron8.cli import set_fact_flags, set_trace
from ultron8.config import do_get_flag, do_set_flag
from ultron8.logging_init import getLogger

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
