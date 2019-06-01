#!/usr/bin/env bash

# set -x

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

py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=ultron8 tests

popd
