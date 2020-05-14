# Example usage:  ultronctl --debug metrics --cluster=local --email=admin@ultron8.com --password=password show

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


@click.group("metrics", short_help="Login to ultron8 cluster")
@click.option(
    "--cluster",
    prompt="Cluster Name",
    confirmation_prompt=False,
    help="Cluster Name eg 'local'",
)
@click.pass_context
def cli(ctx, cluster):
    """
    Login CLI. Used to interact with ultron8 api.
    """
    if ctx.obj["debug"]:
        click.echo("Debug mode initiated")
        set_trace()

    args = {}

    ctx.obj["metrics"] = args
    ctx.obj["metrics"]["cluster"] = cluster.lower()

    ctx.obj["client"].set_api_endpoint(
        ctx.obj["configmanager"].data["clusters"]["instances"][
            ctx.obj["metrics"]["cluster"]
        ]["url"]
    )

    click.secho(
        "Client endpoints: {}\n".format(ctx.obj["client"].endpoints),
        fg=colors.COLOR_SUCCESS,
    )

    if ctx.obj["debug"]:
        click.secho(
            "User: {}\n".format(ctx.obj["metrics"]["email"]), fg=colors.COLOR_SUCCESS
        )
        click.secho(
            "Cluster: {}\n".format(ctx.obj["metrics"]["cluster"]),
            fg=colors.COLOR_SUCCESS,
        )
        click.secho(
            "Cluster url: {}\n".format(ctx.obj["client"].api_endpoint),
            fg=colors.COLOR_SUCCESS,
        )


# @showargs
@cli.command("show")
@click.pass_context
def show(ctx):
    """show command for connecting to a cluster"""
    if ctx.obj["debug"]:
        click.echo("Debug mode initiated")
        set_trace()

    click.secho("metrics show subcommand", fg=colors.COLOR_SUCCESS)

    # response = ctx.obj["client"]._post_metrics_access_show(
    #     ctx.obj["metrics"]["email"], ctx.obj["metrics"]["password"]
    # )

    # click.secho("response: {}\n".format(response), fg=colors.COLOR_SUCCESS)
