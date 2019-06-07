#!/usr/bin/env sh

echo "Running inside /app/prestart.sh, you could add migrations to this file, e.g.:"

# echo "
# #! /usr/bin/env bash

# # Let the DB start
# sleep 10;
# # Run migrations
# alembic upgrade head
# "

pip install -e .

# Let the DB start
sleep 10;
# Run migrations

PYTHONPATH=$(python -c "import sys; print(':'.join(x for x in sys.path if x))")
export PYTHONPATH=${PYTHONPATH}:${ULTRON_WORKDIR}
echo "PYTHONPATH = ${PYTHONPATH}"
echo
# PYTHONPATH=${PYTHONPATH}:ultron8

if [ "$ULTRON_ENABLE_WEB" = true ]; then
    echo " [sourcing] .env.dist"
    . .env.dist
else
    echo " [warning] ULTRON_ENABLE_WEB = false ... skipping sourcing of environment variables"
fi

# Let the DB start
python /home/developer/app/ultron8/api/backend_pre_start.py

echo " [run] alembic upgrade head"
alembic upgrade head

echo " [run] Create initial data in DB"
python /home/developer/app/ultron8/initial_data.py
