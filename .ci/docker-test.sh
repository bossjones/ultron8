#!/bin/bash

set -e

_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
_UID=$(id -u)

PR_SHA=$(git rev-parse HEAD)
REPO_NAME=bossjones/ultron8-ci
IMAGE_TAG=${REPO_NAME}:${PR_SHA}

TAG="${IMAGE_TAG}"

# --security-opt label=disable \
docker run  -i -t \
    --rm \
    --privileged \
    -e "PYENV_VERSION=3.6.8" \
    --volume "$(pwd)/:/home/developer/app:rw" \
    --workdir "/home/developer/app" \
    --entrypoint "bash" \
    "${TAG}" /home/developer/app/.ci/pytest_runner.sh

# /home/developer/app/.ci/tox_runner.sh
