#!/bin/bash

set -e

_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
_UID=$(id -u)

PR_SHA=$(git rev-parse HEAD)
REPO_NAME=bossjones/ultron8-ci
IMAGE_TAG=${REPO_NAME}:${PR_SHA}

TAG="${IMAGE_TAG}"

docker run --rm \
    --security-opt label=disable \
    --privileged \
    --volume "$(pwd)/:/home/developer/app" \
    --workdir "/home/developer/app" \
    "${TAG}" pyenv local 3.6.8;tox -e py36,lint,pylint,cov
