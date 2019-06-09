#!/usr/bin/env bash

# Load utility bash functions
_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $_DIR/utility.sh

# set -x

# trap "echo ERR trap fired!" ERR

# FIXME: I think we need to add these guys to fixuid as well!!! [Jun 3 2019]
# SOURCE: https://github.com/apache/airflow/blob/f153bf536783188bf1db210d30ae44e93a290611/scripts/ci/run-ci.sh
# sudo chown -R airflow.airflow . $HOME/.cache $HOME/.wheelhouse/ $HOME/.cache/pip

echo " [info] CONTAINER_UID=${CONTAINER_UID}"
echo " [info] CONTAINER_GID=${CONTAINER_GID}"
echo

echo " [run] UID/GID map to unknown user/group, \$HOME=/ (the default when no home directory is defined)"
echo -e "\n\n"

eval $( fixuid -q )

echo " [run] UID/GID now match user/group, \$HOME has been set to user's home directory"
echo -e "\n\n"

# gosu developer pyenv shell 3.6.8
# gosu developer pip install -e .
# gosu developer py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=ultron8 tests

pushd /home/developer/app

pyenv shell 3.6.8

pip install -e .


echo " [run] kick off ultron8/api/tests_pre_start.py"
python ultron8/api/tests_pre_start.py

set -eo pipefail

exec py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=ultron8 tests
