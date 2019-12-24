"""
travis tasks
"""
import os
import logging
from invoke import task
from tasks.utils import get_compose_env

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

CI_IMAGE = "bossjones/ultron8-ci"

# .PHONY: travis
# travis: travis-pull travis-build dc-up-web ci-test ## Bring up web server using docker-compose, then exec into container and run pytest
# # tox


@task
def pull(ctx, loc="docker", image=CI_IMAGE):
    """
    Docker pull base and run-image tags
    Usage: inv travis.pull
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    # override CI_IMAGE value
    ctx.config["run"]["env"]["CI_IMAGE"] = image

    _cmds = [
        "docker pull {CI_IMAGE}:base || true".format(CI_IMAGE=image),
        "docker pull {CI_IMAGE}:runtime-image || true".format(CI_IMAGE=image),
    ]

    ctx.run(_cmds[0])
    ctx.run(_cmds[1])
