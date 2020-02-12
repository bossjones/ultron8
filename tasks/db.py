"""
db tasks
"""
import logging
from invoke import task, call
import os
import glob

from urllib.parse import urlparse

# from sqlalchemy.engine.url import make_url
import click
from tasks.utils import get_compose_env, is_venv

from .utils import (
    COLOR_WARNING,
    COLOR_DANGER,
    COLOR_SUCCESS,
    COLOR_CAUTION,
    COLOR_STABLE,
)


# from tasks.core import clean, execute_sql

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


@task(incrementable=["verbose"])
def get_env(ctx, loc="local", verbose=0):
    """
    Get environment vars necessary to run fastapi
    Usage: inv db.get-env
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = False

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    for key in env:
        print("{0}={1}".format(key, env[key]))


@task(incrementable=["verbose"])
def get_python_path(ctx, loc="local", verbose=0):
    """
    Get environment vars necessary to run fastapi
    Usage: inv db.get-python-path
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = 'python -c "import sys; print(sys.executable)"'
    ctx.run(_cmd)


@task(incrementable=["verbose"])
def detect_os(ctx, loc="local", verbose=0):
    """
    detect what type of os we are using
    Usage: inv db.detect-os
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    res_os = ctx.run("uname -s")
    ctx.config["run"]["env"]["OS"] = "{}".format(res_os.stdout)

    if ctx.config["run"]["env"]["OS"] == "Windows_NT":
        ctx.config["run"]["env"]["DETECTED_OS"] = "Windows"
    else:
        ctx.config["run"]["env"]["DETECTED_OS"] = ctx.config["run"]["env"]["OS"]

    if verbose >= 1:
        msg = "[detect-os] Detected: {}".format(ctx.config["run"]["env"]["DETECTED_OS"])
        click.secho(msg, fg=COLOR_SUCCESS)

    if ctx.config["run"]["env"]["DETECTED_OS"] == "Darwin":
        ctx.config["run"]["env"]["ARCHFLAGS"] = "-arch x86_64"
        ctx.config["run"]["env"][
            "PKG_CONFIG_PATH"
        ] = "/usr/local/opt/libffi/lib/pkgconfig"
        ctx.config["run"]["env"]["LDFLAGS"] = "-L/usr/local/opt/openssl/lib"
        ctx.config["run"]["env"]["CFLAGS"] = "-I/usr/local/opt/openssl/include"


@task(pre=[call(detect_os, loc="local")], incrementable=["verbose"])
def autogen(ctx, loc="local", verbose=0, clean=False, dry_run=True, comment=""):
    """
    Autogenerate alembic migration scripts
    Usage: inv db.autogen
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    if verbose >= 1:
        msg = "[autogen] override env vars 'SERVER_NAME' and 'SERVER_HOST' - We don't want to mess w/ '.env.dist' for this situation"
        click.secho(msg, fg=COLOR_SUCCESS)

    if clean:
        if dry_run:
            msg = "[autogen] dry-run mode enabled"
            click.secho(msg, fg=COLOR_CAUTION)
        if verbose >= 1:
            msg = "[autogen] removing existing db first along with items in migration folder"
            click.secho(msg, fg=COLOR_SUCCESS)

        # TODO: 2/10/2020 # Add code to remove both the .db file and the files inside of ultron8/migrations/*.py
        if (
            ctx.config["run"]["env"]["TESTING"]
            and ctx.config["run"]["env"]["TEST_DATABASE_URL"]
        ):
            DATABASE_URL = ctx.config["run"]["env"]["TEST_DATABASE_URL"]
        else:
            DATABASE_URL = ctx.config["run"]["env"]["DATABASE_URL"]

        # get file name, eg dev.db
        dbfile = urlparse(DATABASE_URL).path.replace("/", "")

        # if it exists, nuke it
        if os.path.isfile(dbfile):
            if verbose >= 1:
                _msg = "[autogen] deleting file '{dbfile}'".format(dbfile=dbfile)
                click.secho(_msg, fg=COLOR_SUCCESS)

            if not dry_run:
                ctx.run("rm -fv {dbfile}".format(dbfile=dbfile))
            else:
                _msg = "[autogen] (dry-run) would run rm -fv {dbfile}".format(
                    dbfile=dbfile
                )
                click.secho(_msg, fg=COLOR_CAUTION)

        # open alembic.ini and get path to migration

        versions = glob.glob("ultron8/migrations/versions/*.py")

        if len(versions) > 0:
            for i in versions:
                if verbose >= 1:
                    _msg = "[autogen] git deleting file '{i}'".format(i=i)
                    click.secho(_msg, fg=COLOR_SUCCESS)
                if not dry_run:
                    ctx.run("git rm --force {i}".format(i=i))
                else:
                    _msg = "[autogen] (dry-run) would run git rm -v {i}".format(i=i)
                    click.secho(_msg, fg=COLOR_CAUTION)

    if verbose >= 2:
        _msg = "ctx.config.run.env.TESTING: {}".format(
            ctx.config["run"]["env"]["TESTING"]
        )
        click.secho(_msg, fg=COLOR_SUCCESS)
        _msg = "ctx.config.run.env.TEST_DATABASE_URL: {}".format(
            ctx.config["run"]["env"]["TEST_DATABASE_URL"]
        )
        click.secho(_msg, fg=COLOR_SUCCESS)
        _msg = "ctx.config.run.env.DATABASE_URL: {}".format(
            ctx.config["run"]["env"]["DATABASE_URL"]
        )
        click.secho(_msg, fg=COLOR_SUCCESS)

    # # override CI_IMAGE value
    # ctx.config["run"]["env"]["SERVER_NAME"] = "localhost:11267"
    # ctx.config["run"]["env"]["SERVER_HOST"] = "http://localhost:11267"
    # ctx.config["run"]["env"]["BETTER_EXCEPTIONS"] = "1"

    if not comment:
        _crud_models_cmd = r"""
grep "," ultron8/api/crud/__init__.py | grep -v "^#" | tr ',' '\n' | xargs
"""
        res = ctx.run(_crud_models_cmd)
        # _cmd = "alembic revision --autogenerate -m 'Initial: {comment}'".format(comment=comment)
        _cmd = r"alembic revision --autogenerate -m 'Initial: {comment}'".format(
            comment=res.stdout.rstrip()
        )
    else:
        _cmd = "alembic revision --autogenerate -m 'Initial: {comment}'".format(
            comment=comment
        )

    if verbose >= 1:
        msg = "{}".format(_cmd)
        click.secho(msg, fg=COLOR_SUCCESS)

    if not dry_run:
        ctx.run(_cmd)
    else:
        _msg = "[autogen] (dry-run) would run -> {_cmd}".format(_cmd=_cmd)
        click.secho(_msg, fg=COLOR_CAUTION)
