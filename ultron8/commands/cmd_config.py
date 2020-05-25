import sys


import click

from ultron8.cli import set_trace
from ultron8.config import do_get_flag, show_config
from ultron8.constants import colors
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


@click.group("config", short_help="Manage your ultron8 config")
@click.pass_context
def cli(ctx):
    """config cmds for ultron8."""
    if ctx.obj["debug"]:
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("config subcommand called from cli")


@cli.command("show")
@click.pass_context
def show(ctx):
    """Cmd to show config object for ultron8."""
    if ctx.obj["debug"]:
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("config show subcommand")

    cm = ctx.obj["configmanager"]

    click.secho("Reading config from disk ...\n", fg=colors.COLOR_SUCCESS)
    cm.api.read()

    click.secho(
        "Config Path: {}\n".format(cm.get_cfg_file_path()), fg=colors.COLOR_SUCCESS
    )
    click.secho("{}".format(cm.api.dump()))
