"""
core tasks
"""
import logging
import invoke
from invoke import task
from sqlalchemy.engine.url import make_url
from tasks.utils import get_version, get_compose_env, confirm
from path import Path

PROJROOT = Path(__file__).dirname().parent
# PyBuildRoot = PROJROOT.joinpath('build')
# TrackerRoot = PROJROOT.joinpath('facetracker')

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel("DEBUG")


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
    Usage: inv docker.lint-test or inv local.lint-test
    """
    c.run(
        f"/usr/local/bin/flake8 --ignore=E501,W503 src/ tasks/ tests/ scripts/ migrations/"
    )


@task
def test(c):
    """
    Check Python code style
    Usage: inv docker.test or inv local.test
    """
    c.run(
        f"py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=ultron8 tests"
    )


@task
def test_pdb(c):
    """
    Check Python code style
    Usage: inv docker.test-pdb or inv local.test-pdb
    """
    c.run(
        f"py.test --cov-config .coveragerc --verbose  --pdb --showlocals --cov-report term --cov-report xml --cov=ultron8 tests"
    )


@task
def coverage_run(c):
    """
    Check Python code style
    Usage: inv docker.coverage-run or inv local.coverage-run
    """
    c.run(
        f"coverage run --source=ultron8/ setup.py tests; coverage report --show-missing; coverage html"
    )


@task
def setup_test(c):
    """
    Check Python code style
    Usage: inv docker.setup-test or inv local.setup-test
    """
    c.run(f"python setup.py test")


@task
def run_pytest(c):
    """
    Check Python code style
    Usage: inv docker.run-pytest or inv local.run-pytest
    """
    c.run(
        f"pytest -s --tb short --cov-config .coveragerc --cov ultron8 tests --cov-report term-missing --cov-report xml:cov.xml --cov-report html:htmlcov --cov-report annotate:cov_annotate"
    )


@task
def serve(c):
    """
    Check Python code style
    Usage: inv docker.serve or inv local.serve
    """
    c.run(f"bash script/serve")


@task
def serve_daemon(c):
    """
    Check Python code style
    Usage: inv docker.serve-daemon or inv local.serve-daemon
    """
    c.run(f"bash script/serve-daemon")


@task
def backend_pre_start(c):
    """
    Check Python code style
    Usage: inv docker.backend-pre-start or inv local.backend-pre-start
    """
    c.run(f"python ultron8/api/backend_pre_start.py")


@task
def initial_data(c):
    """
    Check Python code style
    Usage: inv docker.initial-data or inv local.initial-data
    """
    c.run(f"python ultron8/initial_data.py")
