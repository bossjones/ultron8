from typing import Any
from typing import Tuple

import os
import sys

import click

# import pyconfig

from ultron8.logging_init import getLogger

# from ultron8.process import fail
from ultron8.cli import set_trace, set_fact_flags
from ultron8.config import do_get_flag, do_set_flag

logger = getLogger(__name__)

stdin, stdout = sys.stdin, sys.stdout


@click.group("login", short_help="Login to ultron8 cluster")
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
    if do_get_flag("cli.flags.debug"):
        click.echo("Debug mode initiated")
        set_trace()

    click.echo("BLAH")


@cli.command("token")
@click.pass_context
def token(ctx):
    """token command for Workspace"""
    if do_get_flag("cli.flags.debug"):
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("token show subcommand")

    # ctx.obj["workspace"].tree()


# TODO: Create a function to check for access token
# TODO: Create a function request a new access token if it does not exist
# TODO: Update session headers to have access token after you pull it
# TODO: Save access token to disk and use that to pull/verify before making calls
