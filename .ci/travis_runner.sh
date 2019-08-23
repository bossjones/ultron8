#!/usr/bin/env bash

set -x

# Load utility bash functions
_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $_DIR/utility.sh

export TOXENV=py36
export DOCKER_COMPOSE_VERSION=1.24.0
export DOCKER_VERSION=18.09
export IS_CI_ENVIRONMENT="true"
export CACHE_IMAGE=bossjones/ultron8-ci

# docker-compose -f docker-compose.ci.yml pull
docker pull bossjones/ultron8-ci:runtime-image
make ci-build
make ci-test
