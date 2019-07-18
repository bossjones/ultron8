"""Gathers environment settings and loads them into global attributes for Api service."""
import logging
import os
import sys

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
from starlette.datastructures import Secret

log = logging.getLogger(__name__)


LOG_LEVEL_MAP = {
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "WARNING": logging.WARN,
    "WARN": logging.WARN,
    "ERROR": logging.ERROR,
    "FATAL": logging.FATAL,
    "CRITICAL": logging.CRITICAL,
}


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


API_V1_STR = "/v1"

DEFAULT_SECRET_KEY = b"supersecretkey"

SECRET_KEY = os.getenvb(b"SECRET_KEY", DEFAULT_SECRET_KEY)
if not SECRET_KEY:
    SECRET_KEY = os.urandom(32)

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days


SERVER_NAME = os.getenv("SERVER_NAME")
SERVER_HOST = os.getenv("SERVER_HOST")
PROJECT_NAME = os.getenv("PROJECT_NAME")
SENTRY_DSN = os.getenv("SENTRY_DSN")

SMTP_TLS = getenv_boolean("SMTP_TLS", True)
SMTP_PORT = None
_SMTP_PORT = os.getenv("SMTP_PORT")
if _SMTP_PORT is not None:
    SMTP_PORT = int(_SMTP_PORT)
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAILS_FROM_EMAIL = os.getenv("EMAILS_FROM_EMAIL")
EMAILS_FROM_NAME = PROJECT_NAME
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 48
EMAIL_TEMPLATES_DIR = "/app/app/email-templates/build"
EMAILS_ENABLED = SMTP_HOST and SMTP_PORT and EMAILS_FROM_EMAIL

USERS_OPEN_REGISTRATION = getenv_boolean("USERS_OPEN_REGISTRATION")

# # ORIGINALLY THIS!!!!!!!!!!!!!!!!!!!!! 6/4/2019
# # config = Config(".env")
# config = Config(".env.dist")

# # # Main Configs
# DEBUG = config("DEBUG", cast=bool, default=False)
# TESTING = config("TESTING", cast=bool, default=False)
# # SECRET_KEY = config('SECRET_KEY', cast=Secret)
# # ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings)

# # # Redis
# # REDIS_ENDPOINT = config('REDIS_ENDPOINT', default='127.0.0.1')
# # REDIS_PORT = config('REDIS_PORT', default=6379, cast=int)
# # REDIS_DB = config('REDIS_DB', default=0, cast=int)
# # REDIS_PASSWORD = config('REDIS_PASSWORD', default=None, cast=Secret)

# # DB
# DATABASE_URL = config("DATABASE_URL")

# # Testing
# TEST_DATABASE_URL = config("TEST_DATABASE_URL")

# -------------------------------------------------------------------------------
# # Main Configs
DEBUG = getenv_boolean("DEBUG", True)
# bool(os.environ.get("DEBUG", False))
# TESTING = bool(os.environ.get("TESTING", False))
TESTING = getenv_boolean("TESTING", False)
TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL", None)

if TESTING and TEST_DATABASE_URL:
    DATABASE_URL = TEST_DATABASE_URL
else:
    DATABASE_URL = os.environ.get("DATABASE_URL", None)

BACKEND_CORS_ORIGINS = os.getenv(
    "BACKEND_CORS_ORIGINS", "*"
)  # a string of origins separated by commas, e.g: "http://localhost, http://localhost:4200, http://localhost:3000, http://localhost:8080, http://local.dockertoolbox.tiangolo.com"

FIRST_SUPERUSER = os.getenv("FIRST_SUPERUSER", "admin")
FIRST_SUPERUSER_PASSWORD = os.getenv("FIRST_SUPERUSER_PASSWORD", "password")

_USER_LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_LEVEL = LOG_LEVEL_MAP[_USER_LOG_LEVEL]
MASK_SECRETS = getenv_boolean("MASK_SECRETS", True)
