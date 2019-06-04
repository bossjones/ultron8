#!/usr/bin/env bash

eval $( fixuid -q )

if [ "$ULTRON_ENABLE_WEB" = true ]; then
    source .env.dist
fi

exec /start-gunicorn.sh
