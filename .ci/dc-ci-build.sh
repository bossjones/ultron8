#!/bin/bash

set -e

_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONTAINER_UID=$(id -u)
CONTAINER_GID=$(id -g)

PR_SHA=$(git rev-parse HEAD)
REPO_NAME=bossjones/ultron8-ci
IMAGE_TAG=${REPO_NAME}:${PR_SHA}

TAG="${IMAGE_TAG}"

docker-compose -f docker-compose.ci.yml build
