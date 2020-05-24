import os
import sys

from typing import Any, Tuple

import click

from ultron8.cli import set_fact_flags, set_trace
from ultron8.config import do_get_flag, do_set_flag
from ultron8.logging_init import getLogger

logger = getLogger(__name__)

stdin, stdout = sys.stdin, sys.stdout


@click.group("workspace", short_help="All commands dealing with workspace for ultron8")
@click.pass_context
def cli(ctx):
    """Interact with workspace for ultron8."""
    if ctx.obj["debug"]:
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("workspace subcommand called from cli")
    ctx.obj["workspace"].setup()


@cli.command("tree")
@click.pass_context
def tree(ctx):
    """Tree command for Workspace"""
    if ctx.obj["debug"]:
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("tree show subcommand")

    ctx.obj["workspace"].tree()


@cli.command("info")
@click.pass_context
def info(ctx):
    """Info on workspace"""
    if ctx.obj["debug"]:
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("workspace infosubcommand")

    click.echo("--------------------------------")
    click.echo("-------[Workspace Info]---------")
    click.echo("--------------------------------")
    click.echo("Root: {}".format(ctx.obj["workspace"]._root))
    click.echo("Api: {}".format(ctx.obj["workspace"].api))
    click.echo("Workdir: {}".format(ctx.obj["workspace"]._wdir))
    click.echo("Libdir: {}".format(ctx.obj["workspace"]._lib_dir))
    click.echo("Templatedir: {}".format(ctx.obj["workspace"]._template_dir))


# @click.group("cluster", short_help="Manage your ultron8 clusters")
# @click.pass_context
# def cli(ctx):
#     """cluster cmds for ultron8."""
#     if ctx.obj["debug"]:
#         click.echo("Debug mode initiated")
#         set_trace()

#     logger.debug("cluster subcommand called from cli")


# @cli.command("setup")
# @click.argument("cluster_url", envvar="ULTRON_CLUSTER_URL")
# @click.pass_context
# def setup(ctx, cluster_url):
#     """Cmd to setup workspace etc for ultron8."""
#     if ctx.obj["debug"]:
#         click.echo("Debug mode initiated")
#         set_trace()

#     logger.debug("cluster setup subcommand")
