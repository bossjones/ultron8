#!/bin/bash

echo "[Initializing pyenv] ...."
export PYENV_ROOT="/.pyenv" \
export PATH="/.pyenv/bin:/.pyenv/shims:$PATH"
export CFLAGS='-O2'
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
source /.pyenv/completions/pyenv.bash


echo "[Configured, enjoy pyenv] ...."
env | grep PYENV
