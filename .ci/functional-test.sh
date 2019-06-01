#!/bin/bash

# This has to be the first command because BASH_SOURCE[0] gets changed.
SCRIPT=${BASH_SOURCE[0]:-$0}

[[ "${BASH_SOURCE[0]}" == "$0" ]] \
    && echo "This script should not be executed but sourced like:" \
    && echo "    $ source $0" \
    && echo \
    && exit 1



_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
_UID=$(id -u)

tox -e py36 --notest && \
make install && \
pyenv rehash

# && \
# moonbeam-cli --help && \
# moonbeam-cli config_init && \
# cat /home/developer/.config/moonbeam_cli/config.yaml; \
# moonbeam-cli moonbeam_service_config_init
