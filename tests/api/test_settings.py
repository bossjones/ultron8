"""Test settings."""
# pylint: disable=protected-access
import logging
import os
import errno
import unittest
import unittest.mock as mock

import pytest

# import ultron8.config
# from tests import helper
from ultron8.api.settings import getenv_boolean
from ultron8.api.settings import SettingsConfig


# SOURCE: https://github.com/ansible/ansible/blob/370a7ace4b3c8ffb6187900f37499990f1b976a2/test/units/module_utils/basic/test_atomic_move.py


@pytest.fixture
def atomic_mocks(mocker, monkeypatch):
    environ = dict()
    mocks = {
        "chmod": mocker.patch("os.chmod"),
        "chown": mocker.patch("os.chown"),
        "close": mocker.patch("os.close"),
        "environ": mocker.patch("os.environ", environ),
        "getlogin": mocker.patch("os.getlogin"),
        "getuid": mocker.patch("os.getuid"),
        "path_exists": mocker.patch("os.path.exists"),
        "rename": mocker.patch("os.rename"),
        "stat": mocker.patch("os.stat"),
        "umask": mocker.patch("os.umask"),
        "getpwuid": mocker.patch("pwd.getpwuid"),
        "copy2": mocker.patch("shutil.copy2"),
        "copyfileobj": mocker.patch("shutil.copyfileobj"),
        "move": mocker.patch("shutil.move"),
        "mkstemp": mocker.patch("tempfile.mkstemp"),
    }

    mocks["getlogin"].return_value = "developer"
    mocks["getuid"].return_value = 501
    mocks["getpwuid"].return_value = ("developer", "", 501, 501, "", "", "")
    mocks["umask"].side_effect = [18, 0]
    mocks["rename"].return_value = None

    # pwd.struct_passwd(pw_name='malcolm', pw_passwd='********', pw_uid=501, pw_gid=20, pw_gecos='Malcolm Jones', pw_dir='/Users/malcolm', pw_shell='/bin/bash')

    # normalize OS specific features
    monkeypatch.delattr(os, "chflags", raising=False)

    yield mocks


@pytest.fixture(scope="function")
def fake_environ(mocker, monkeypatch):
    orig_environ = os.environ
    environ = dict()
    environ["DEBUG"] = "True"
    environ["TESTING"] = "True"
    environ["SECRET_KEY"] = "43n080musdfjt54t-09sdgr"
    environ["REDIS_URL"] = "redis://localhost"
    environ["REDIS_ENDPOINT"] = "127.0.0.1"
    environ["REDIS_PORT"] = "6379"
    environ["REDIS_DB"] = "0"
    environ["DATABASE_URL"] = "sqlite:///dev.db"
    environ["TEST_DATABASE_URL"] = "sqlite:///test.db"
    environ["DEFAULT_MODULE_NAME"] = "ultron8.web"
    environ["VARIABLE_NAME"] = "app"
    environ["MODULE_NAME"] = "ultron8.web"
    environ["APP_MODULE"] = "ultron8.web:app"
    # environ["DEFAULT_GUNICORN_CONF"] = /Users/malcolm/dev/bossjones/ultron8/gunicorn_conf.py
    # environ["PRE_START_PATH"] = /Users/malcolm/dev/bossjones/ultron8/migrations/gunicorn-prestart.sh
    environ["DOMAIN"] = "localhost"
    environ["HOST"] = "localhost"
    environ["PORT"] = "11267"
    environ["LOG_LEVEL"] = logging.DEBUG
    environ["BETTER_EXCEPTIONS"] = "1"
    environ["SERVER_NAME"] = "localhost:11267"
    environ["SERVER_HOST"] = "http://localhost:11267"
    environ["ULTRON_ENABLE_WEB"] = "False"
    environ[
        "JUPYTER"
    ] = "jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888"
    environ["PROJECT_NAME"] = "ultron8"
    environ["DOMAIN_MAIN"] = "ultron8.com"
    environ["FIRST_SUPERUSER"] = "admin@ultron8.com"
    environ["FIRST_SUPERUSER_PASSWORD"] = "password"
    environ["SMTP_TLS"] = "True"
    environ["SMTP_PORT"] = "587"
    environ["SMTP_EMAILS_FROM_EMAIL"] = "info@ultron8.com"
    environ["FLOWER_AUTH"] = "admin:password"
    environ["USERS_OPEN_REGISTRATION"] = "False"
    environ["BACKEND_CORS_ORIGINS"] = "*"

    mocks = {"environ": mocker.patch("os.environ", environ)}

    yield mocks


@pytest.mark.settingsonly
@pytest.mark.unittest
def test_getenv_boolean(fake_environ):
    assert getenv_boolean("SMTP_TLS") is True


# # FIXME: Todo, make sure these values get coerced into what they should be.
# @pytest.mark.settingsonly
# @pytest.mark.unittest
# def test_SettingsConfig(fake_environ):
#     # from ultron8.debugger import dump_magic

#     # sc = SettingsConfig()

#     # dump_magic(fake_environ)

#     assert fake_environ["environ"]["DEBUG"] == SettingsConfig.DEBUG
#     assert fake_environ["environ"]["TESTING"] == SettingsConfig.TESTING
#     assert fake_environ["environ"]["SECRET_KEY"] == SettingsConfig.SECRET_KEY
#     # assert fake_environ["environ"]["REDIS_URL"] == SettingsConfig.REDIS_URL
#     # assert fake_environ["environ"]["REDIS_ENDPOINT"] == SettingsConfig.REDIS_ENDPOINT
#     # assert fake_environ["environ"]["REDIS_PORT"] == SettingsConfig.REDIS_PORT
#     # assert fake_environ["environ"]["REDIS_DB"] == SettingsConfig.REDIS_DB
#     assert fake_environ["environ"]["DATABASE_URL"] == SettingsConfig.DATABASE_URL
#     assert fake_environ["environ"]["TEST_DATABASE_URL"] == SettingsConfig.TEST_DATABASE_URL
#     # assert fake_environ["environ"]["DEFAULT_MODULE_NAME"] == SettingsConfig.DEFAULT_MODULE_NAME
#     # assert fake_environ["environ"]["VARIABLE_NAME"] == SettingsConfig.VARIABLE_NAME
#     # assert fake_environ["environ"]["MODULE_NAME"] == SettingsConfig.MODULE_NAME
#     # assert fake_environ["environ"]["APP_MODULE"] == SettingsConfig.APP_MODULE
#     # assert fake_environ["environ"]["DOMAIN"] == SettingsConfig.DOMAIN
#     # assert fake_environ["environ"]["HOST"] == SettingsConfig.HOST
#     # assert fake_environ["environ"]["PORT"] == SettingsConfig.PORT
#     assert fake_environ["environ"]["LOG_LEVEL"] == SettingsConfig.LOG_LEVEL
#     # assert fake_environ["environ"]["BETTER_EXCEPTIONS"] == SettingsConfig.BETTER_EXCEPTIONS
#     assert fake_environ["environ"]["SERVER_NAME"] == SettingsConfig.SERVER_NAME
#     assert fake_environ["environ"]["SERVER_HOST"] == SettingsConfig.SERVER_HOST
#     # assert fake_environ["environ"]["ULTRON_ENABLE_WEB"] == SettingsConfig.ULTRON_ENABLE_WEB
#     # assert fake_environ["environ"]["JUPYTER"] == SettingsConfig.JUPYTER
#     assert fake_environ["environ"]["PROJECT_NAME"] == SettingsConfig.PROJECT_NAME
#     # assert fake_environ["environ"]["DOMAIN_MAIN"] == SettingsConfig.DOMAIN_MAIN
#     assert fake_environ["environ"]["FIRST_SUPERUSER"] == SettingsConfig.FIRST_SUPERUSER
#     assert fake_environ["environ"]["FIRST_SUPERUSER_PASSWORD"] == SettingsConfig.FIRST_SUPERUSER_PASSWORD
#     assert fake_environ["environ"]["SMTP_TLS"] == SettingsConfig.SMTP_TLS
#     assert fake_environ["environ"]["SMTP_PORT"] == SettingsConfig.SMTP_PORT
#     # assert fake_environ["environ"]["SMTP_EMAILS_FROM_EMAIL"] == SettingsConfig.SMTP_EMAILS_FROM_EMAIL
#     # assert fake_environ["environ"]["FLOWER_AUTH"] == SettingsConfig.FLOWER_AUTH
#     assert fake_environ["environ"]["USERS_OPEN_REGISTRATION"] == SettingsConfig.USERS_OPEN_REGISTRATION
#     assert fake_environ["environ"]["BACKEND_CORS_ORIGINS"] == SettingsConfig.BACKEND_CORS_ORIGINS
