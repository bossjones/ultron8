#!/usr/bin/env bash

# set -x

# trap "echo ERR trap fired!" ERR

echo " [info] CONTAINER_UID=${CONTAINER_UID}"
echo " [info] CONTAINER_GID=${CONTAINER_GID}"
echo

echo " [run] UID/GID map to unknown user/group, \$HOME=/ (the default when no home directory is defined)"
echo -e "\n\n"

eval $( fixuid -q )

echo " [run] UID/GID now match user/group, \$HOME has been set to user's home directory"
echo -e "\n\n"

# FIXME: Add a flag to enable gosu when needed
# gosu developer pyenv shell 3.6.8
# gosu developer pip install -e .
# gosu developer py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=ultron8 tests

pushd /home/developer/app

pyenv shell 3.6.8

pip install -e .

set -eo pipefail
py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=ultron8 tests

popd
