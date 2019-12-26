"""
local tasks
"""
import logging
from invoke import task, call
import os
from sqlalchemy.engine.url import make_url
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


# @task
# def run_local(c, service='flask'):
#     if not is_venv():
#         raise Exception("Venv is not activated. Please activate the onboarding \
#             venv by running $ROOT_REPO/venv/bin/activate.")
#     env = get_compose_env(c)
#     if service == 'flask':
#         c.run("flask run --reload --host 0.0.0.0 --port 5000 --debugger", env=env)
#     else:
#         print('Unknown service')

# @task
# def start_db(c):
#     env = get_compose_env(c)
#     c.run('docker-compose  -f ./aws-codebuild/dev-stack.yaml up -d adminer', env=env)


# @task
# def reset_test_db(c, loc='local'):
#     """
#     Reset the test database
#     """
#     conn_string = c.local['env']['TEST_SQLALCHEMY_DATABASE_URI']
#     db = make_url(conn_string)
#     sql1 = f'DROP DATABASE IF EXISTS {db.database}'
#     sql2 = f'CREATE DATABASE {db.database}'
#     execute_sql(c, sql=[sql1, sql2],
#                 conn_string=conn_string, database='template1')


@task(incrementable=["verbose"],)
def get_env(ctx, loc="local", verbose=0):
    """
    Get environment vars necessary to run fastapi
    Usage: inv local.get-env
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = False

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    for key in env:
        print("{0}={1}".format(key, env[key]))


@task(incrementable=["verbose"],)
def get_python_path(ctx, loc="local", verbose=0):
    """
    Get environment vars necessary to run fastapi
    Usage: inv local.get-python-path
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = 'python -c "import sys; print(sys.executable)"'
    ctx.run(_cmd)


@task(incrementable=["verbose"],)
def detect_os(ctx, loc="local", verbose=0):
    """
    detect what type of os we are using
    Usage: inv local.detect-os
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
        res_detected_os = ctx.run("uname -s")
        ctx.config["run"]["env"]["DETECTED_OS"] = "{}".format(res_detected_os.stdout)

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


@task(
    pre=[call(detect_os, loc="local"),], incrementable=["verbose"],
)
def serve(ctx, loc="local", verbose=0, cleanup=False):
    """
    start up fastapi application
    Usage: inv local.serve
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    if verbose >= 1:
        msg = "[serve] override env vars 'SERVER_NAME' and 'SERVER_HOST' - We don't want to mess w/ '.env.dist' for this situation"
        click.secho(msg, fg=COLOR_SUCCESS)

    # override CI_IMAGE value
    ctx.config["run"]["env"]["SERVER_NAME"] = "localhost:11267"
    ctx.config["run"]["env"]["SERVER_HOST"] = "http://localhost:11267"
    ctx.config["run"]["env"]["BETTER_EXCEPTIONS"] = "1"

    _cmd = r"""
pkill -f "ultron8/dev_serve.py" || true
pgrep -f "ultron8/dev_serve.py" || true
    """

    if verbose >= 1:
        msg = "[serve] kill running app server: "
        click.secho(msg, fg=COLOR_SUCCESS)

        msg = "{}".format(_cmd)
        click.secho(msg, fg=COLOR_SUCCESS)

    ctx.run(_cmd)

    ctx.run("pip install -e .")
    ctx.run("alembic --raiseerr upgrade head")
    ctx.run("python ./ultron8/api/backend_pre_start.py")
    ctx.run("python ./ultron8/initial_data.py")
    ctx.run("python ultron8/dev_serve.py")
