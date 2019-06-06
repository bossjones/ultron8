#! /usr/bin/env sh

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
    source .env.dist
fi

# Let the DB start
python /home/developer/app/ultron8/backend_pre_start.py

echo " [run] alembic upgrade head"
alembic upgrade head
