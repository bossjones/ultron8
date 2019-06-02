#!/bin/bash

#############################################################
# NOTE: This entrypoint script is only used to test individual testing suites!
# If you want to run everything, just call test-all-experimental.sh
#############################################################

set -e

# Load utility bash functions
_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $_DIR/utility.sh

# Move to our working directory since this will be called via entrypoint
cd /spark-app

CURRENT_ARG="$1"

if [ "$1" = "bash" ]; then
    shift
    exec bash "$@"
elif [ "$1" = "sh" ]; then
    shift
    exec sh "$@"
elif [ "$1" = "python" ]; then
    shift
    exec python "$@"
elif [ "$1" = "ipython" ]; then
    shift
    exec ipython -i "$@"
elif [ "$1" = "fake8" ]; then
    shift
    header "Running be-personalization flake8"
    exec flake8 --verbose --max-line-length=200 --exclude=.venv,.git,.tox,docs,www_static,venv,bin,lib,deps,build --ignore=E302,E401,E501,E265,E713,E402,D204,D102,D400,D205,E402,D202,D103,D209,D105,D101,D401,D200,E127,D100 /spark-app/app /spark-app/tests
elif [ "$1" = "isort" ]; then
    shift
    header "Running be-personalization isort"
    exec isort --recursive --check-only --diff --verbose /spark-app/app /spark-app/tests
elif [ "$1" = "pylint" ]; then
    shift
    header "Running be-personalization pylint"
    exec pylint --rcfile ./pylintrc ./app/const.py
elif [ "$1" = "pytest" ]; then
    shift
    header "Running be-personalization pytest"
    exec pytest -c /spark-app/pytest.ini --cov=/spark-app/app --pep8
elif [ "$1" = "coverage" ]; then
    shift
    header "Running be-personalization coverage"
    # FIXME: to make .app importable, we need to add it to PYTHONPATH :( ...
    # turning this into a properly setup python package would get around this issue
    export PYTHONPATH="/spark-app/:/spark-app/tests:$PYTHONPATH"
    exec pytest --timeout=60 -c /spark-app/pytest.ini --cov=/spark-app/app --cov-report term-missing
else
    # NOTE: default test. If you can at least 'import pyspark',
    # then you have your environment setup correctly
    log "INFO" "arg1 = $CURRENT_ARG"
    header "Running be-personalization sys.path test for pyspark"
    exec python -c 'import pyspark'
fi
