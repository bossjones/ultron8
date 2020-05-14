# Example usage:  ultronctl --debug login --cluster=local --email=admin@ultron8.com --password=password token

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

from ultron8.constants import colors

logger = getLogger(__name__)

stdin, stdout = sys.stdin, sys.stdout

# SOURCE: https://stackoverflow.com/questions/2088056/get-kwargs-inside-function
def showargs(function):
    """Get kwargs Inside Function

    Arguments:
        function {[type]} -- [description]
    """

    def inner(*args, **kwargs):
        return function((args, kwargs), *args, **kwargs)

    return inner


@click.group("login", short_help="Login to ultron8 cluster")
@click.option(
    "--cluster",
    prompt="Cluster Name",
    confirmation_prompt=False,
    help="Cluster Name eg 'local'",
)
@click.option(
    "--email", prompt="Email", confirmation_prompt=False, help="Email",
)
@click.option(
    "--password",
    prompt="Password",
    hide_input=True,
    confirmation_prompt=False,
    help="Password",
)
@click.pass_context
def cli(ctx, cluster, email, password):
    """
    Login CLI. Used to interact with ultron8 api.
    """
    if ctx.obj["debug"]:
        click.echo("Debug mode initiated")
        set_trace()

    args = {}

    ctx.obj["login"] = args
    ctx.obj["login"]["cluster"] = cluster
    ctx.obj["login"]["email"] = email
    ctx.obj["login"]["password"] = password

    ctx.obj["client"].set_api_endpoint(
        ctx.obj["configmanager"].data.clusters.instances.local.url
    )

    click.secho(
        "Client endpoints: {}\n".format(ctx.obj["client"].endpoints),
        fg=colors.COLOR_SUCCESS,
    )

    if ctx.obj["debug"]:
        click.secho(
            "User: {}\n".format(ctx.obj["login"]["email"]), fg=colors.COLOR_SUCCESS
        )
        click.secho(
            "Cluster: {}\n".format(ctx.obj["login"]["cluster"]), fg=colors.COLOR_SUCCESS
        )
        click.secho(
            "Cluster url: {}\n".format(ctx.obj["client"].api_endpoint),
            fg=colors.COLOR_SUCCESS,
        )


# @showargs
@cli.command("token")
@click.pass_context
def token(ctx):
    """token command for connecting to a cluster"""
    if ctx.obj["debug"]:
        click.echo("Debug mode initiated")
        set_trace()

    click.secho("login token subcommand", fg=colors.COLOR_SUCCESS)

    response = ctx.obj["client"]._post_login_access_token(
        ctx.obj["login"]["email"], ctx.obj["login"]["password"]
    )

    click.secho("response: {}\n".format(response), fg=colors.COLOR_SUCCESS)


# TODO: Create a function to check for access token
# TODO: Create a function request a new access token if it does not exist
# TODO: Update session headers to have access token after you pull it
# TODO: Save access token to disk and use that to pull/verify before making calls
