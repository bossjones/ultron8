#!/usr/bin/env bash

# Load utility bash functions
_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $_DIR/utility.sh

eval $( fixuid -q )

pushd /home/developer/app

pyenv shell 3.6.8

pip install -e .

set -eo pipefail

header " [run] tail -f /dev/null"

exec tail -f /dev/null

# popd
