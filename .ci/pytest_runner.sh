#!/usr/bin/env bash

set -x

# UID/GID map to unknown user/group, $HOME=/ (the default when no home directory is defined)

eval $( fixuid )

# UID/GID now match user/group, $HOME has been set to user's home directory

# gosu developer pyenv shell 3.6.8

# gosu developer pip install -e .

# gosu developer py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=ultron8 tests

pyenv shell 3.6.8

pip install -e .

py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=ultron8 tests
