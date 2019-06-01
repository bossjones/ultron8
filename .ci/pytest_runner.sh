#!/usr/bin/env bash

set -x

pip install -e .

py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=ultron8 tests
