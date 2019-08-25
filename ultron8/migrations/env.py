from __future__ import with_statement

import logging
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from ultron8.api import settings
from ultron8.api.db.u_sqlite.base import Base
from ultron8.web import app

from ultron8.api.middleware.logging import log

log.setup_logging()

##############################
# EVERYTHING YOU NEED TO KNOW ABOUT SQLITE
# https://docs.sqlalchemy.org/en/13/dialects/sqlite.html
# https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#module-sqlalchemy.dialects.sqlite.pysqlite
##############################

# NOTE: If debug logging is enabled, then turn on debug logging for everything in app
if settings.LOG_LEVEL == logging.DEBUG:

    # Enable connection pool logging
    # SOURCE: https://docs.sqlalchemy.org/en/13/core/engines.html#dbengine-logging
    SQLALCHEMY_POOL_LOGGER = logging.getLogger("sqlalchemy.pool")
    SQLALCHEMY_ENGINE_LOGGER = logging.getLogger("sqlalchemy.engine")
    SQLALCHEMY_ORM_LOGGER = logging.getLogger("sqlalchemy.orm")
    SQLALCHEMY_DIALECTS_LOGGER = logging.getLogger("sqlalchemy.dialects")
    SQLALCHEMY_POOL_LOGGER.setLevel(logging.DEBUG)
    SQLALCHEMY_ENGINE_LOGGER.setLevel(logging.DEBUG)
    SQLALCHEMY_ORM_LOGGER.setLevel(logging.DEBUG)
    SQLALCHEMY_DIALECTS_LOGGER.setLevel(logging.DEBUG)

if settings.DEBUG_REQUESTS:
    # import requests.packages.urllib3.connectionpool as http_client
    # http_client.HTTPConnection.debuglevel = 1
    REQUESTS_LOGGER = logging.getLogger("requests")
    REQUESTS_LOGGER.setLevel(logging.DEBUG)
    REQUESTS_LOGGER.propagate = True
    URLLIB3_LOGGER = logging.getLogger("urllib3")
    URLLIB3_LOGGER.setLevel(logging.DEBUG)

LOGGER = logging.getLogger(__name__)


# from ultron8.debugger import debug_dump_exclude

# https://stackoverflow.com/questions/15648284/alembic-alembic-revision-says-import-error
# parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
# here = os.path.abspath(os.path.dirname(__file__))
# print(f"here: {here}")
# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# print(f"parent_dir: {parent_dir}")
# sys.path.append(parent_dir)
# from ultron8.api.db.u_sqlite import metadata
# pylint: disable=no-name-in-module
# from ultron8.api.db.base import Base  # noqa
# from ultron8.api.db.u_sqlite.base_class import Base

# pylint: disable=maybe-no-member
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

if settings.DATABASE_URL is None:
    raise ValueError(
        "You are attempting to run a migration without having 'settings.DATABASE_URL' set, please set environment value and try again."
    )

LOGGER.info("settings.DATABASE_URL = %s" % str(settings.DATABASE_URL))
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

# debug_dump_exclude(settings)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# fileConfig(config.config_file_name)
fileConfig(config.config_file_name, disable_existing_loggers=False)

# import pdb;pdb.set_trace()

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# def get_url():
#     user = os.getenv("POSTGRES_USER", "postgres")
#     password = os.getenv("POSTGRES_PASSWORD", "")
#     server = os.getenv("POSTGRES_SERVER", "db")
#     db = os.getenv("POSTGRES_DB", "app")
#     return f"postgresql://{user}:{password}@{server}/{db}"

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    # TODO: Enable postgres version 7/23/2019 # url = get_url()
    # TODO: Enable postgres version 7/23/2019 # context.configure(
    # TODO: Enable postgres version 7/23/2019 #     url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    # TODO: Enable postgres version 7/23/2019 # )

    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                LOGGER.info("No changes in schema detected.")

    # TODO: Enable postgres version 7/23/2019 # configuration = config.get_section(config.config_ini_section)
    # TODO: Enable postgres version 7/23/2019 # configuration['sqlalchemy.url'] = get_url()
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
        )

        try:
            with context.begin_transaction():
                context.run_migrations()
        finally:
            connection.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
