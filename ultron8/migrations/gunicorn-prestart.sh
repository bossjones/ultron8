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
echo "PYTHONPATH = ${PYTHONPATH}"
echo
PYTHONPATH=${PYTHONPATH}:ultron8 alembic upgrade head
