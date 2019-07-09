#!/bin/bash

set -e

_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
_UID=$(id -u)

PR_SHA=dev
REPO_NAME=bossjones/ultron8-ci
IMAGE_TAG=${REPO_NAME}:${PR_SHA}

TAG="${IMAGE_TAG}"

docker run -i -t \
    --rm \
    --security-opt label=disable \
    --privileged \
    --volume "$(pwd)/:/home/developer/app" \
    --workdir "/home/developer/app" \
    --entrypoint "/bin/bash" \
    "${TAG}" -l
