"""
ci tasks
"""
import os
import logging
from invoke import task
from tasks.utils import get_compose_env

# from tasks.core import clean, execute_sql

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


@task
def pylint(ctx, loc="local"):
    """
    pylint ultron8 folder
    Usage: inv ci.pylint
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    ctx.run(
        "pylint --disable=all --enable=F,E --rcfile ./lint-configs-python/python/pylintrc ultron8"
    )


@task
def mypy(ctx, loc="local"):
    """
    mypy ultron8 folder
    Usage: inv ci.mypy
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    ctx.run("mypy --config-file ./lint-configs-python/python/mypy.ini ultron8 tests")


@task
def black(ctx, loc="local"):
    """
    black ultron8 folder
    Usage: inv ci.black
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    ctx.run("black --check --exclude=ultron8_venv* --verbose ultron8")


@task
def isort(ctx, loc="local"):
    """
    isort ultron8 folder
    Usage: inv ci.isort
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    ctx.run("isort --recursive --check-only --diff --verbose ultron8 tests")
