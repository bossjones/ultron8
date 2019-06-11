#!/bin/bash

set -e

_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export CONTAINER_UID=$(id -u)
export CONTAINER_GID=$(id -g)

PR_SHA=$(git rev-parse HEAD)
REPO_NAME=bossjones/ultron8-ci
IMAGE_TAG=${REPO_NAME}:${PR_SHA}

TAG="${IMAGE_TAG}"

docker pull $REPO_NAME:base || true
docker pull $REPO_NAME:runtime-image || true
docker-compose -f docker-compose.base.yml build
docker push $REPO_NAME:base || true

docker pull $REPO_NAME:runtime-image || true
docker-compose -f docker-compose.ci.yml build
docker push $REPO_NAME:runtime-image || true
