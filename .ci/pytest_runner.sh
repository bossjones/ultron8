#!/usr/bin/env bash

set -x

gosu developer pip install -e .

gosu developer py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=ultron8 tests
