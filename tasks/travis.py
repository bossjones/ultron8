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


@task
def container_uid(ctx, loc="docker"):
    """
    Docker container_uid base and run-image tags
    Usage: inv travis.container_uid
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    res = ctx.run("id -u")

    ctx.config["run"]["env"]["CONTAINER_UID"] = "{}".format(res.stdout)


@task
def container_gid(ctx, loc="docker"):
    """
    Docker container_gid base and run-image tags
    Usage: inv travis.container_gid
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    res = ctx.run("id -g")

    ctx.config["run"]["env"]["CONTAINER_GID"] = "{}".format(res.stdout)


# .PHONY: ci-build
# ci-build: ci-before_install dc-build-cache-base dc-up-web ci-gunzip # build docker cache base, cache it locally on machine and send up to docker hub etc


@task
def build_gunzip_before_install(ctx, loc="docker", image=CI_IMAGE):
    """
    docker container/image from gnzip tar file in $HOME/.cache/docker
    Usage: inv travis.build_gunzip_before_install
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    # override CI_IMAGE value
    ctx.config["run"]["env"]["CI_IMAGE"] = image
    ctx.config["run"]["env"]["CACHE_DIR"] = "$HOME/.cache/docker"
    ctx.config["run"]["env"]["CACHE_FILE_BASE"] = "$CACHE_DIR/base.tar.gz"
    ctx.config["run"]["env"]["CACHE_FILE_RUNTIME"] = "$CACHE_DIR/runtime-image.tar.gz"

    # export CACHE_DIR=$HOME/.cache/docker
    # export CACHE_FILE_BASE=$CACHE_DIR/base.tar.gz
    # export CACHE_FILE_RUNTIME=$CACHE_DIR/runtime-image.tar.gz

    # export CONTAINER_UID=$(id -u)
    # export CONTAINER_GID=$(id -g)

    # PR_SHA=$(git rev-parse HEAD)
    # REPO_NAME=bossjones/ultron8-ci
    # IMAGE_TAG=${REPO_NAME}:${PR_SHA}

    # TAG="${IMAGE_TAG}"

    _cmd = "docker-compose -f docker-compose.ci.yml build"

    ctx.run(_cmd)
