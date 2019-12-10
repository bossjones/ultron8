#!/usr/bin/env bash

# Activate the virtual environment before running inv comannds

pyenv activate ultron8_venv374

envs=$(inv local.get-env)
for e in $envs; do unset $( echo $e | cut -d '=' -f1); done
for e in $envs; do export $e; done
