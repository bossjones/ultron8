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


@click.command("login", short_help="Login to ultron8 cluster")
@click.option("--user", prompt="Username", help="Username")
@click.option(
    "--password",
    prompt="Password",
    hide_input=True,
    confirmation_prompt=True,
    help="Password",
)
@click.option(
    "--password-stdin",
    prompt="Take the password from stdin",
    help="Take the password from stdin",
)
@click.pass_context
def cli(ctx, user, password, password_stdin):
    """
    Login CLI. Used to interact with ultron8 api.
    """
    if get_flag("debug"):
        click.echo("Debug mode initiated")
        set_trace()

    click.echo("BLAH")
