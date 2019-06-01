#!/bin/bash

# set -e

_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
_UID=$(id -u)

echo "[ci] pulling base container bossjones/ultron8-hacking"
docker pull bossjones/ultron8-hacking:0.1.0

PR_SHA=$(git rev-parse HEAD)
REPO_NAME=bossjones/ultron8-ci
IMAGE_TAG=${REPO_NAME}:${PR_SHA}

TAG="${IMAGE_TAG}"

docker build \
    --build-arg CONTAINER_UID="${_UID}" \
    --tag "${TAG}" \
    --file "Dockerfile" $(pwd)

