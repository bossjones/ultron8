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

# gosu developer pyenv shell 3.7.4
# gosu developer pip install -e .
# gosu developer py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=ultron8 tests

set -x
pushd /home/developer/app

pyenv shell 3.7.4

pip install -e .

echo " [run] alembic upgrade head"
alembic upgrade head

echo " [run] kick off ultron8/api/tests_pre_start.py"
python ultron8/api/tests_pre_start.py

set -eo pipefail

# exec py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=ultron8 tests
exec py.test --cov-config .coveragerc --verbose --cov-append --cov-report term-missing --cov-report xml:cov.xml --cov-report html:htmlcov --cov-report annotate:cov_annotate --mypy --showlocals --tb=short --cov=ultron8 tests
