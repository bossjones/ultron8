#!/bin/bash

set -e

_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Load utility bash functions
source $_DIR/utility.sh

if [ "IS_CI_ENVIRONMENT" == "true" ]; then
    export CONTAINER_UID=$(ls -lta | awk '{print $3}')
    export CONTAINER_GID=$(ls -lta | awk '{print $4}')

    export CI_BUILD_NUMBER="$TRAVIS_BUILD_NUMBER"
    export CI_PULL_REQUEST="$TRAVIS_PULL_REQUEST"
    export CI_BRANCH="$TRAVIS_BRANCH"

else
    export CONTAINER_UID=$(id -u)
    export CONTAINER_GID=$(id -g)
fi

PR_SHA=$(git rev-parse HEAD)
REPO_NAME=bossjones/ultron8-ci
IMAGE_TAG=${REPO_NAME}:${PR_SHA}

TAG="${IMAGE_TAG}"

header " [run] docker ps -a"
docker ps -a


_NUM_STOPPED_CONTAINER=$(docker ps -a| grep -v PORTS | grep Exited | awk '{print $1}' | wc -l)

header " [info] _NUM_STOPPED_CONTAINER=${_NUM_STOPPED_CONTAINER}"

set -x

if [[ "${_NUM_STOPPED_CONTAINER}" -gt "0" ]]; then
    _CONTAINER_ID=$(docker ps -a -q --no-trunc | head -1)
    docker logs ${_CONTAINER_ID}
fi

set +x

header " [run] test container <ultron8_ci> using /home/developer/app/.ci/pytest_runner.sh"
# -T Disable pseudo-tty allocation. By default `docker-compose exec` allocates a TTY.
time docker-compose -f docker-compose.ci.yml exec -T ultron8_ci /home/developer/app/.ci/pytest_runner.sh
