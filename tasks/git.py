"""
git tasks
"""
import logging
from invoke import task
import os
from tasks.utils import get_compose_env, is_venv

# from tasks.core import clean, execute_sql

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


# git rev-parse HEAD


@task
def pr_sha(ctx, loc="local"):
    """
    Return `git rev-parse HEAD` for project.
    Usage: inv docker.lint-test or inv local.lint-test
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = False

    res = ctx.run("git rev-parse HEAD")

    return res.stdout
