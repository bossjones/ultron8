# Example usage: ultronctl user --cluster=local list

from typing import Any
from typing import Tuple

import json

import os
import sys
import pprint

import click

from ultron8.logging_init import getLogger

# from ultron8.process import fail
from ultron8.cli import set_trace, set_fact_flags
from ultron8.config import do_get_flag, do_set_flag


from ultron8.constants import colors

import termtables as tt
from ultron8.api.models.user import UserCreate
from fastapi.encoders import jsonable_encoder

logger = getLogger(__name__)

TERMTABLES_HEADER = ["ID", "Email", "Full Name", "Is Active", "Is Superuser"]

pp = pprint.PrettyPrinter(indent=4)

stdin, stdout = sys.stdin, sys.stdout


def user_results_to_list(user_dict):
    return [
        user_dict["id"],
        user_dict["email"],
        user_dict["full_name"],
        user_dict["is_active"],
        user_dict["is_superuser"],
    ]


@click.group("user", short_help="User CLI. Used to interact with ultron8 api")
@click.option(
    "--cluster",
    prompt="Cluster Name",
    confirmation_prompt=False,
    help="Cluster Name eg 'local'",
)
@click.pass_context
def cli(ctx, cluster):
    """
    User CLI. Used to interact with ultron8 api.
    """
    args = {}

    ctx.obj["user"] = args
    ctx.obj["user"]["cluster"] = cluster

    # Set api endpoint on client
    ctx.obj["client"].set_api_endpoint(
        ctx.obj["configmanager"].data["clusters"]["instances"][
            ctx.obj["user"]["cluster"]
        ]["url"]
    )

    # Grab access token from config and set it on client
    ctx.obj["client"].jwt_token = ctx.obj["configmanager"].data["clusters"][
        "instances"
    ][ctx.obj["user"]["cluster"]]["token"]

    if ctx.obj["debug"]:
        click.secho(
            "Cluster: {}\n".format(ctx.obj["user"]["cluster"]), fg=colors.COLOR_SUCCESS
        )
        click.secho(
            "Cluster url: {}\n".format(ctx.obj["client"].api_endpoint),
            fg=colors.COLOR_SUCCESS,
        )


@cli.command("list")
@click.option(
    "--output",
    type=click.Choice(["table", "json"], case_sensitive=True),
    default="table",
    help=("Format results by either table or json "),
    show_default=True,
)
@click.pass_context
def list(ctx, output):
    """list command for users"""
    if ctx.obj["debug"]:
        click.echo("Debug mode initiated")
        set_trace()

    ctx.obj["user"]["output"] = output

    click.secho("user list subcommand", fg=colors.COLOR_SUCCESS)

    # Run API call
    response = ctx.obj["client"]._get_users()

    # Output values
    click.secho("response: \n\n", fg=colors.COLOR_SUCCESS)

    if ctx.obj["user"]["output"] == "table":

        data = [user_results_to_list(i) for i in response]

        tt.print(
            data, header=TERMTABLES_HEADER, style=tt.styles.double,
        )

    else:
        pp.pprint(response)

    click.secho("\n\n", fg=colors.COLOR_SUCCESS)


@cli.command("create")
@click.option(
    "--payload", type=click.File("r"), help=("Payload in json format"),
)
@click.option(
    "--output",
    type=click.Choice(["table", "json"], case_sensitive=True),
    default="json",
    help=("Format results by either table or json "),
    show_default=True,
)
@click.pass_context
def create(ctx, payload, output):
    """create user from payload"""
    if ctx.obj["debug"]:
        click.echo("Debug mode initiated")
        set_trace()

    click.secho("user create subcommand", fg=colors.COLOR_SUCCESS)

    ctx.obj["user"]["output"] = output

    source = json.load(payload)
    click.secho("Data loaded: \n\n", fg=colors.COLOR_SUCCESS)
    click.secho("{}".format(source), fg=colors.COLOR_SUCCESS)

    # data = UserCreate(email=source["email"], password=source["password"])
    data = {"email": source["email"], "password": source["password"]}

    json_compatible_data = jsonable_encoder(data)

    click.secho("data: \n\n", fg=colors.COLOR_SUCCESS)
    click.secho("{}".format(data), fg=colors.COLOR_SUCCESS)

    # Run API call
    response = ctx.obj["client"]._post_create_user(json_compatible_data)

    # Output values
    click.secho("response: \n\n", fg=colors.COLOR_SUCCESS)

    if ctx.obj["user"]["output"] == "table":

        data = [user_results_to_list(i) for i in response]

        tt.print(
            data, header=TERMTABLES_HEADER, style=tt.styles.double,
        )

    else:
        pp.pprint(response)

    click.secho("\n\n", fg=colors.COLOR_SUCCESS)
