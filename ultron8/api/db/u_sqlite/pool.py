"""Initialize the DB pool.

Use the `database` attribute as your interface to the db.
"""
import logging
import databases
from ultron8.api import settings

log = logging.getLogger(__name__)

if settings.TESTING:
    database = databases.Database(settings.TEST_DATABASE_URL, force_rollback=True)
else:
    database = databases.Database(settings.DATABASE_URL)


async def open_database_connection_pool():
    await database.connect()


async def close_database_connection_pool():
    await database.disconnect()
