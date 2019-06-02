#!/usr/bin/env bash

eval $( fixuid -q )

exec /start-gunicorn.sh
