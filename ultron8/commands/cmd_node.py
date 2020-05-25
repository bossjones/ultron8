import sys


import click

from ultron8.cli import set_fact_flags, set_trace
from ultron8.config import do_get_flag, do_set_flag
from ultron8.logging_init import getLogger

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
    if ctx.obj["debug"]:
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("View Ultron8 node information")


@cli.command("show")
@click.pass_context
def show(ctx):
    """Show Ultron8 node information"""
    if ctx.obj["debug"]:
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("node show subcommand")
