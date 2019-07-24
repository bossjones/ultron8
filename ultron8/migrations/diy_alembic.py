#!/usr/bin/env python

import traceback

import better_exceptions

better_exceptions.hook()

import sys

from IPython.core.debugger import Tracer  # noqa
from IPython.core import ultratb

sys.excepthook = ultratb.FormattedTB(
    mode="Verbose", color_scheme="Linux", call_pdb=True, ostream=sys.__stdout__
)

# import os
import argparse
from alembic import __version__ as __alembic_version__
from alembic.config import Config as AlembicConfig
from alembic import command
from alembic.util import CommandError
import inspect
from functools import wraps

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
from ultron8.debugger import debug_dump_exclude

log.setup_logging()

LOGGER = logging.getLogger(__name__)

# logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

alembic_version = tuple([int(v) for v in __alembic_version__.split(".")[0:3]])


def catch_errors(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except (CommandError, RuntimeError, TypeError) as exc:
            LOGGER.error("Error: " + str(exc))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            LOGGER.error("exc_type: " + str(exc_type))
            LOGGER.error("exc_value: " + str(exc_value))
            traceback.print_tb(exc_traceback)
            # sys.exit(1)
            raise

    return wrapped


# NOTE: ASSUMES THIS DIRECTORY STRUCTURE
# .                         # root dir
# |- alembic/               # directory with migrations
# |- tests/diy_alembic.py   # example script
# |- alembic.ini            # ini file

# SOURCE: https://stackoverflow.com/questions/24622170/using-alembic-api-from-inside-application-code
@catch_errors
def alembic_upgrade():
    # set the paths values
    this_file_directory = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
    root_directory = os.path.join(this_file_directory, "..", "..")
    alembic_directory = this_file_directory
    ini_path = os.path.join(root_directory, "alembic.ini")

    # LOGGER.info(f"this_file_directory = {this_file_directory}")
    # LOGGER.info(f"root_directory = {root_directory}")
    # LOGGER.info(f"alembic_directory = {alembic_directory}")
    # LOGGER.info(f"ini_path = {ini_path}")

    # create Alembic config and feed it with paths
    config = AlembicConfig(ini_path)
    # print(config.get_section("alembic"))
    LOGGER.info(f"get_section(alembic) = %s" % (config.get_section("alembic")))
    LOGGER.info(f"get_section(loggers) = %s" % (config.get_section("loggers")))
    LOGGER.info(f"get_section(handlers) = %s" % (config.get_section("handlers")))
    LOGGER.info(f"get_section(formatters) = %s" % (config.get_section("formatters")))
    LOGGER.info(f"get_section(logger_root) = %s" % (config.get_section("logger_root")))
    LOGGER.info(
        f"get_section(logger_sqlalchemy) = %s"
        % (config.get_section("logger_sqlalchemy"))
    )
    LOGGER.info(
        f"get_section(logger_alembic) = %s" % (config.get_section("logger_alembic"))
    )
    LOGGER.info(
        f"get_section(handler_console) = %s" % (config.get_section("handler_console"))
    )

    config.set_main_option("script_location", alembic_directory)
    # config.cmd_opts = argparse.Namespace()   # arguments stub

    # prepare and run the command
    revision = "head"
    sql = False
    tag = None

    # upgrade command
    # try:
    # import pdb;pdb.set_trace()
    command.upgrade(config, revision, sql=sql, tag=tag)
    # except
    # alembic upgrade head


alembic_upgrade()
