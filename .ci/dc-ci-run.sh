#!/bin/bash

set -e

_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ "IS_CI_ENVIRONMENT" == "true" ]; then
    export CONTAINER_UID=$(ls -lta | awk '{print $3}')
    export CONTAINER_GID=$(ls -lta | awk '{print $4}')
else
    export CONTAINER_UID=$(id -u)
    export CONTAINER_GID=$(id -g)
fi

PR_SHA=$(git rev-parse HEAD)
REPO_NAME=bossjones/ultron8-ci
IMAGE_TAG=${REPO_NAME}:${PR_SHA}

TAG="${IMAGE_TAG}"

exec docker-compose -f docker-compose.ci.yml run ultron8_ci /home/developer/app/.ci/pytest_runner.sh
