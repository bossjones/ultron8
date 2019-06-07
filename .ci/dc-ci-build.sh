#!/bin/bash

set -e

_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export CONTAINER_UID=$(id -u)
export CONTAINER_GID=$(id -g)

PR_SHA=$(git rev-parse HEAD)
REPO_NAME=bossjones/ultron8-ci
IMAGE_TAG=${REPO_NAME}:${PR_SHA}

TAG="${IMAGE_TAG}"

# docker build \
#       --build-arg CONTAINER_UID="${CONTAINER_UID}" \
#       --build-arg CONTAINER_GID="${CONTAINER_GID}" \
#       --target base \
#       --cache-from $REPO_NAME:base \
#       --tag $REPO_NAME:base \
#       --file "Dockerfile" $(pwd)

docker-compose -f docker-compose.ci.yml build
