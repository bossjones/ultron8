"""
local tasks
"""
import logging
from invoke import task
import os
from sqlalchemy.engine.url import make_url
from tasks.utils import get_compose_env, is_venv

# from tasks.core import clean, execute_sql

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


# @task
# def run_local(c, service='flask'):
#     if not is_venv():
#         raise Exception("Venv is not activated. Please activate the onboarding \
#             venv by running $ROOT_REPO/venv/bin/activate.")
#     env = get_compose_env(c)
#     if service == 'flask':
#         c.run("flask run --reload --host 0.0.0.0 --port 5000 --debugger", env=env)
#     else:
#         print('Unknown service')

# @task
# def start_db(c):
#     env = get_compose_env(c)
#     c.run('docker-compose  -f ./aws-codebuild/dev-stack.yaml up -d adminer', env=env)


# @task
# def reset_test_db(c, loc='dev'):
#     """
#     Reset the test database
#     """
#     conn_string = c.dev['env']['TEST_SQLALCHEMY_DATABASE_URI']
#     db = make_url(conn_string)
#     sql1 = f'DROP DATABASE IF EXISTS {db.database}'
#     sql2 = f'CREATE DATABASE {db.database}'
#     execute_sql(c, sql=[sql1, sql2],
#                 conn_string=conn_string, database='template1')


@task
def get_env(c):
    """
    Get environment vars necessary to run flask
    Usage: inv local.get-env
    """
    env = get_compose_env(c)
    for key in env:
        print("{0}={1}".format(key, env[key]))
