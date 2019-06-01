#!/usr/bin/env bash

set -x

py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=ultron8 tests
