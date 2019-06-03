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

pyenv shell 3.6.8

pip install -e .

set -eo pipefail

exec flake8 --select=E --max-line-length=200 --exclude=.venv,.git,.tox,docs,www_static,venv,bin,lib,deps,build --ignore=E302,E401,E501,E265,E713,E402,D204,D102,D400,D205,E402,D202,D103,D209,D105,D101,D401,D200,E127,D100 /home/developer/app/ultron8 /home/developer/app/tests
