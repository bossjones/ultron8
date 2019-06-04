"""Gathers environment settings and loads them into global attributes for Api service."""
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

import logging

log = logging.getLogger(__name__)


config = Config(".env")

# # Main Configs
DEBUG = config("ULTRON_DEBUG", cast=bool, default=False)
TESTING = config("ULTRON_TESTING", cast=bool, default=False)
# SECRET_KEY = config('ULTRON_SECRET_KEY', cast=Secret)
# ALLOWED_HOSTS = config('ULTRON_ALLOWED_HOSTS', cast=CommaSeparatedStrings)

# # Redis
# REDIS_ENDPOINT = config('ULTRON_REDIS_ENDPOINT', default='127.0.0.1')
# REDIS_PORT = config('ULTRON_REDIS_PORT', default=6379, cast=int)
# REDIS_DB = config('ULTRON_REDIS_DB', default=0, cast=int)
# REDIS_PASSWORD = config('ULTRON_REDIS_PASSWORD', default=None, cast=Secret)

# DB
DATABASE_URL = config("ULTRON_DATABASE_URL")

# Testing
TEST_DATABASE_URL = config("ULTRON_TEST_DATABASE_URL")
