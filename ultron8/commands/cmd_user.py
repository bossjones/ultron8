from typing import Any
from typing import Tuple

import os
import sys

import click

from ultron8.logging_init import getLogger

# from ultron8.process import fail
from ultron8.cli import set_trace, set_fact_flags
from ultron8.config import do_get_flag, do_set_flag

logger = getLogger(__name__)

stdin, stdout = sys.stdin, sys.stdout


@click.command("user", short_help="User CLI. Used to interact with ultron8 api")
@click.option(
    "-m",
    "--method",
    type=click.Choice(["GET", "POST", "PUT", "DELETE"], case_sensitive=False),
)
@click.pass_context
def cli(ctx, method):
    """
    User CLI. Used to interact with ultron8 api.
    """
    if do_get_flag("cli.flags.debug"):
        click.echo("Debug mode initiated")
        set_trace()

    click.echo("BLAH")
