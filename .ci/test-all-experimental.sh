#!/bin/bash

# TODO: Enable this when you're ready to start fixing tests
# set -e

# Load utility bash functions
_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $_DIR/utility.sh

# Move to our working directory since this will be called via entrypoint
cd /spark-app

echo ""
header "Running be-personalization sys.path test for pyspark"
python -c 'import pyspark'
echo ""

echo ""
header "Running be-personalization flake8"
flake8 --ignore=E302,E401,E501,E265,E713,E402,D204,D102,D400,D205,E402,D202,D103,D209,D105,D101,D401,D200,E127,D100 /spark-app/app /spark-app/tests
echo ""

echo ""
header "Running be-personalization isort"
isort --recursive --check-only --diff --verbose /spark-app/app /spark-app/tests
echo ""

echo ""
header "Running be-personalization pylint"
pylint --rcfile ./pylintrc ./app/const.py
echo ""

echo ""
header "Running be-personalization pytest"
pytest -c /spark-app/pytest.ini --cov=/spark-app/app --pep8
echo ""

echo ""
header "Running be-personalization coverage"
# FIXME: to make .app importable, we need to add it to PYTHONPATH :( ...
# turning this into a properly setup python package would get around this issue
export PYTHONPATH="/spark-app/:/spark-app/tests:$PYTHONPATH"
pytest --timeout=60 -c /spark-app/pytest.ini --cov=/spark-app/app --cov-report term-missing
echo ""
