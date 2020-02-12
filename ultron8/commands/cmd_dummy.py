from typing import Any
from typing import Tuple

import os
import sys

import click

# import pyconfig

from ultron8.logging_init import getLogger

# from ultron8.process import fail
from ultron8.cli import set_trace, get_flag

logger = getLogger(__name__)

stdin, stdout = sys.stdin, sys.stdout


@click.command("dummy", short_help="Dummy command, doesn't do anything.")
@click.pass_context
def cli(ctx):
    """
    Dummy command, doesn't do anything.
    """
    if get_flag("debug"):
        click.echo("Debug mode initiated")
        set_trace()

    if get_flag("debug"):
        click.echo("[DUMP ctx]: ")
        for k, v in ctx.obj.items():
            click.echo(f"  {k} -> {v}")

    click.echo("Dummy command, doesn't do anything.")

    if ctx.obj["verbose"] > 0:
        click.echo("Ran [{}]| test".format(sys._getframe().f_code.co_name))
