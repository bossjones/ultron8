#!/bin/bash

# SOURCE: http://rundef.com/fast-travis-ci-docker-build

set -e

_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Load utility bash functions
source $_DIR/utility.sh

export CACHE_DIR=$HOME/.cache/docker
export CACHE_FILE_BASE=$CACHE_DIR/base.tar.gz
export CACHE_FILE_RUNTIME=$CACHE_DIR/runtime-image.tar.gz

export CONTAINER_UID=$(id -u)
export CONTAINER_GID=$(id -g)

PR_SHA=$(git rev-parse HEAD)
REPO_NAME=bossjones/ultron8-ci
IMAGE_TAG=${REPO_NAME}:${PR_SHA}

TAG="${IMAGE_TAG}"

header " [run] travis 'before_install:' section"
if [ -f ${CACHE_FILE_BASE} ]; then gunzip -c ${CACHE_FILE_BASE} | docker load || true; fi
if [ -f ${CACHE_FILE_RUNTIME} ]; then gunzip -c ${CACHE_FILE_RUNTIME} | docker load || true; fi

