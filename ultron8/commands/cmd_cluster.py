from typing import Any
from typing import Tuple

import os
import sys

import click

from ultron8.logging_init import getLogger

from ultron8.cli import set_trace, get_flag, set_fact_flags

logger = getLogger(__name__)

stdin, stdout = sys.stdin, sys.stdout

# for reference use: https://docs.d2iq.com/mesosphere/dcos/2.0/cli/


@click.command("cluster", short_help="Manage your ultron8 clusters")
@click.pass_context
def cli(ctx):
    """cluster cmd to setup workspace etc for ultron8."""
    if get_flag("debug"):
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("cluster subcommand called from cli")
