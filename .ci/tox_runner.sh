#!/usr/bin/env bash

set -x

pyenv local 3.7.4;tox -e py37,lint,pylint,cov
