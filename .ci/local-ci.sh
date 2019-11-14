#!/usr/bin/env bash

# SOURCE: http://rundef.com/fast-travis-ci-docker-build

set -e

_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Load utility bash functions
source $_DIR/utility.sh

source .local.dist

# run tests
python setup.py test
