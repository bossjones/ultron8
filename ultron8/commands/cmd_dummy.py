import os
import sys

from typing import Any, Tuple

import click

# from ultron8.process import fail
# from ultron8.cli import set_trace, get_flag
from ultron8.cli import set_trace
from ultron8.config import do_get_flag, do_set_flag
from ultron8.logging_init import getLogger

# import pyconfig


logger = getLogger(__name__)

stdin, stdout = sys.stdin, sys.stdout


@click.group("dummy", short_help="Dummy command, doesn't do anything.")
@click.pass_context
def cli(ctx):
    """
    Dummy command, doesn't do anything.
    """
    if do_get_flag("cli.flags.debug"):
        click.echo("Debug mode initiated")
        set_trace()

    if do_get_flag("cli.flags.debug"):
        click.echo("[DUMP ctx]: ")
        for k, v in ctx.obj.items():
            click.echo(f"  {k} -> {v}")

    click.echo("Dummy command, doesn't do anything.")

    if ctx.obj["verbose"] > 0:
        click.echo("Ran [{}]| test".format(sys._getframe().f_code.co_name))
