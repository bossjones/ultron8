from typing import Any
from typing import Tuple

import os
import sys

import click

# import pyconfig

from ultron8.logging_init import getLogger

# from ultron8.process import fail
from ultron8.cli import cli, set_trace, get_flag

logger = getLogger(__name__)

stdin, stdout = sys.stdin, sys.stdout


@cli.command()
@click.pass_context
def login(ctx):
    """
    User CLI. Used to interact with ultron8 api.
    """
    if get_flag("debug"):
        click.echo("Debug mode initiated")
        set_trace()

    click.echo("BLAH")
