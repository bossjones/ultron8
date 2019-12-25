"""
travis tasks
"""
import os
import logging
from invoke import task, call
from tasks.utils import get_compose_env

from .git import pr_sha

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

CI_IMAGE = "bossjones/ultron8-ci"

# .PHONY: travis
# travis: travis-pull travis-build dc-up-web ci-test ## Bring up web server using docker-compose, then exec into container and run pytest
# # tox


@task(incrementable=["verbose"])
def pull(ctx, loc="docker", image=CI_IMAGE, verbose=0):
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


@task(incrementable=["verbose"])
def container_uid(ctx, loc="docker", verbose=0):
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


@task(incrementable=["verbose"])
def container_gid(ctx, loc="docker", verbose=0):
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


@task(incrementable=["verbose"])
def pip_cache(ctx, loc="docker", verbose=0):
    """
    Configure pip cache env vars
    Usage: inv travis.pip_cache
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    ctx.config["run"]["env"]["STANDARD_CACHE_DIR"] = "~/.cache/pip"
    ctx.config["run"]["env"]["WHEELHOUSE"] = "{}/wheels".format(
        ctx.config["run"]["env"]["STANDARD_CACHE_DIR"]
    )
    ctx.config["run"]["env"]["PIP_WHEEL_DIR"] = "{}".format(
        ctx.config["run"]["env"]["WHEELHOUSE"]
    )

    # ctx.config["run"]["env"]["CONTAINER_GID"] = "{}".format(res.stdout)
    # SOURCE: https://blog.ionelmc.ro/2015/01/02/speedup-pip-install/
    # export STANDARD_CACHE_DIR="${XDG_CACHE_HOME:-${HOME}/.cache}/pip"
    # export WHEELHOUSE="${STANDARD_CACHE_DIR}/wheels"
    # export PIP_FIND_LINKS="file://${WHEELHOUSE}"
    # export PIP_WHEEL_DIR="${WHEELHOUSE}"


@task(incrementable=["verbose"])
def env_set(ctx, loc="docker", image=CI_IMAGE, verbose=0):
    """
    Configure env for travis builds
    Usage: inv travis.env-set
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
    ctx.config["run"]["env"]["IS_CI_ENVIRONMENT"] = "true"


@task(
    pre=[
        call(pr_sha, loc="docker"),
        call(container_uid, loc="docker"),
        call(container_gid, loc="docker"),
        call(pip_cache, loc="docker"),
        call(env_set, loc="docker"),
    ],
    incrementable=["verbose"],
)
def preflight(ctx, loc="docker", image=CI_IMAGE, verbose=0):
    """
    Configure env for travis builds
    Usage: inv travis.env-set
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _VALIDATE_ENVS = [
        "CI_IMAGE",
        "CACHE_DIR",
        "CACHE_FILE_BASE",
        "CACHE_FILE_RUNTIME",
        "IS_CI_ENVIRONMENT",
        "CONTAINER_UID",
        "CONTAINER_GID",
        "TAG",
        "STANDARD_CACHE_DIR",
        "WHEELHOUSE",
        "PIP_WHEEL_DIR",
    ]

    # Verify everything has been set that we care about.
    # TODO: Move this into its own private task, so it can be called from anywhere
    for v in _VALIDATE_ENVS:
        assert ctx.config["run"]["env"][v]


# .PHONY: ci-build
# ci-build: ci-before_install dc-build-cache-base dc-up-web ci-gunzip # build docker cache base, cache it locally on machine and send up to docker hub etc


@task(
    pre=[
        call(pr_sha, loc="docker"),
        call(container_uid, loc="docker"),
        call(container_gid, loc="docker"),
    ],
    incrementable=["verbose"],
)
def build_gunzip_before_install(ctx, loc="docker", image=CI_IMAGE, verbose=0):
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
    ctx.config["run"]["env"]["IS_CI_ENVIRONMENT"] = "true"

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
