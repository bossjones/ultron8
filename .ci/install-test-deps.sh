#!/bin/bash

set -e

# Move to our working directory since this will be called via entrypoint
cd /spark-app

# FIXME: Implement bash check to see if pytest is installed with specific version number, if not run pip install
pip install --no-cache-dir -r requirements_test.txt
