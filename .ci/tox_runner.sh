#!/usr/bin/env bash

set -x

pyenv local 3.6.8;tox -e py36,lint,pylint,cov
