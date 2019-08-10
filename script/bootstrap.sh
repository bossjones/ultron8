#!/usr/bin/env bash
# -*- coding: utf-8 -*-

set -e

_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#--- User Defined Variable ---
PACKAGE_NAME="ultron8"

# Python version Used for Development
PY_VER_MAJOR="3"
PY_VER_MINOR="6"
PY_VER_MICRO="8"

export PROJECT_NAME="${PACKAGE_NAME}"

export PYTHON_VERSION="${PY_VER_MAJOR}.${PY_VER_MINOR}.${PY_VER_MICRO}"
export PYENV_NAME="${PACKAGE_NAME}_venv"

# Vars Dir
export ROOT_DIR
ROOT_DIR=$(pwd)
