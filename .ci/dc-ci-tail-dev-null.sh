#!/bin/bash

set -e

trap "{ pkill -f tail }" EXIT SIGINT SIGTERM

_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export CONTAINER_UID=$(id -u)
export CONTAINER_GID=$(id -g)

PR_SHA=$(git rev-parse HEAD)
REPO_NAME=bossjones/ultron8-ci
IMAGE_TAG=${REPO_NAME}:${PR_SHA}

TAG="${IMAGE_TAG}"

exec docker-compose -f docker-compose.ci.yml run ultron8_ci /home/developer/app/.ci/tail_dev_null_runner.sh
