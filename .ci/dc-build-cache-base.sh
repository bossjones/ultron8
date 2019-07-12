#!/bin/bash

set -e

_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Load utility bash functions
source $_DIR/utility.sh

export CONTAINER_UID=$(id -u)
export CONTAINER_GID=$(id -g)

PR_SHA=$(git rev-parse HEAD)
REPO_NAME=bossjones/ultron8-ci
IMAGE_TAG=${REPO_NAME}:${PR_SHA}

TAG="${IMAGE_TAG}"

header " [run] pull docker cache from docker hub if available"
time docker pull $REPO_NAME:base || true
time docker pull $REPO_NAME:runtime-image || true
header " [run] docker-compose build 'base'"
time docker-compose -f docker-compose.base.yml build
header " [run] docker-compose push '$REPO_NAME:base'"
time docker push $REPO_NAME:base || true

header " [run] docker-compose pull '$REPO_NAME:runtime-image'"
time docker pull $REPO_NAME:runtime-image || true
header " [run] docker-compose build '$REPO_NAME:runtime-image'"
time docker-compose -f docker-compose.ci.yml build
header " [run] docker-compose push '$REPO_NAME:runtime-image'"
time docker push $REPO_NAME:runtime-image || true
