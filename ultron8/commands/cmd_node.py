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

# ##############################################################################
# # Catch exceptions and go into ipython/ipdb

# from IPython.core.debugger import Tracer  # noqa
# from IPython.core import ultratb

# sys.excepthook = ultratb.FormattedTB(
#     mode="Verbose", color_scheme="Linux", call_pdb=True, ostream=sys.__stdout__
# )
# ##############################################################################

# for reference use: https://docs.d2iq.com/mesosphere/dcos/2.0/cli/


@click.group("node", short_help="Manage your ultron8 nodes")
@click.pass_context
def cli(ctx):
    """View Ultron8 node information."""
    if do_get_flag("cli.flags.debug"):
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("View Ultron8 node information")


@cli.command("show")
@click.pass_context
def show(ctx):
    """Show Ultron8 node information"""
    if do_get_flag("cli.flags.debug"):
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("node show subcommand")
