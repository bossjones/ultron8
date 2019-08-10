#!/usr/bin/env bash
# -*- coding: utf-8 -*-

# shellcheck source=/dev/null
[ -r "script/bootstrap.sh" ] && source "script/bootstrap.sh"

cat <<EOF
-----------------------
    Initiate Pyenv
-----------------------
EOF

# load source files externals
if [ -e "$HOME/.pyenv" ]; then
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
fi

cd "${ROOT_DIR}" || exit

cat <<EOF
-----------------------
    Initiate Pyenv Virtualenv
-----------------------
EOF

pyenv virtualenv "${PYTHON_VERSION}" "${PYENV_NAME}" >> /dev/null 2>&1 || echo 'Oh Yeah!!'

# https://github.com/luismayta/dotfiles/blob/597ddc09e1bfccc43076ca21cb679299b83912e4/conf/shell/zshrc
# alias reload!='exec "$SHELL" -l'
