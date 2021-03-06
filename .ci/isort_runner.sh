#!/usr/bin/env bash

# Load utility bash functions
_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $_DIR/utility.sh

echo " [info] CONTAINER_UID=${CONTAINER_UID}"
echo " [info] CONTAINER_GID=${CONTAINER_GID}"
echo

echo " [run] UID/GID map to unknown user/group, \$HOME=/ (the default when no home directory is defined)"
echo -e "\n\n"

eval $( fixuid -q )

echo " [run] UID/GID now match user/group, \$HOME has been set to user's home directory"
echo -e "\n\n"

pushd /home/developer/app

pyenv shell 3.7.4

pip install -e .

set -eo pipefail

exec isort --recursive --check-only --diff --verbose /home/developer/app/ultron8 /home/developer/app/tests
