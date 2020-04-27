from typing import Any
from typing import Tuple

import os
import sys

import click

from ultron8.logging_init import getLogger

from ultron8.cli import set_trace, set_fact_flags
from ultron8.config import do_get_flag, do_set_flag

logger = getLogger(__name__)

stdin, stdout = sys.stdin, sys.stdout


@click.group("workspace", short_help="All commands dealing with workspace for ultron8")
@click.pass_context
def cli(ctx):
    """Interact with workspace for ultron8."""
    if do_get_flag("cli.flags.debug"):
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("workspace subcommand called from cli")


@cli.command("tree")
@click.pass_context
def tree(ctx):
    """Tree command for Workspace"""
    if do_get_flag("cli.flags.debug"):
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("tree show subcommand")

    ctx.obj["workspace"].tree()


# @click.group("cluster", short_help="Manage your ultron8 clusters")
# @click.pass_context
# def cli(ctx):
#     """cluster cmds for ultron8."""
#     if do_get_flag("cli.flags.debug"):
#         click.echo("Debug mode initiated")
#         set_trace()

#     logger.debug("cluster subcommand called from cli")


# @cli.command("setup")
# @click.argument("cluster_url", envvar="ULTRON_CLUSTER_URL")
# @click.pass_context
# def setup(ctx, cluster_url):
#     """Cmd to setup workspace etc for ultron8."""
#     if do_get_flag("cli.flags.debug"):
#         click.echo("Debug mode initiated")
#         set_trace()

#     logger.debug("cluster setup subcommand")
