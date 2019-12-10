"""
core tasks
"""
import logging
from invoke import task
from sqlalchemy.engine.url import make_url
from tasks.utils import get_version, get_compose_env, confirm

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


@task
def clean(c, docs=False, bytecode=True, extra=""):
    """[summary]

    Arguments:
        c {[type]} -- [description]

    Keyword Arguments:
        docs {bool} -- [description] (default: {False})
        bytecode {bool} -- [description] (default: {True})
        extra {str} -- [description] (default: {''})
    """
    c.run("find . -name '*.pyc' -delete")


@task
def lint_tests(c):
    """
    Check Python code style
    Usage: inv dev.lint-test
    """
    c.run(
        f"/usr/local/bin/flake8 --ignore=E501,W503 src/ tasks/ tests/ scripts/ migrations/"
    )


# test="py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=ultron8 tests"
# test-pdb="py.test --cov-config .coveragerc --verbose  --pdb --showlocals --cov-report term --cov-report xml --cov=ultron8 tests"
# coverage-run="coverage run --source=ultron8/ setup.py tests; coverage report --show-missing; coverage html"
# setup-test="python setup.py test"
# # NOTE: This one taken from bemoonbeam_cli
# run-pytest="pytest -s --tb short --cov-config .coveragerc --cov ultron8 tests --cov-report term-missing --cov-report xml:cov.xml --cov-report html:htmlcov --cov-report annotate:cov_annotate"
# serve = "bash script/serve"
# serve-daemon = "bash script/serve-daemon"
# migrate = "alembic upgrade head"
# backend_pre_start = "python ultron8/api/backend_pre_start.py"
# initial_data = "python ultron8/initial_data.py"
