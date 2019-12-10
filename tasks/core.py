"""
core tasks
"""
import logging
from pathlib import Path
import invoke
from invoke import task
from sqlalchemy.engine.url import make_url
from tasks.utils import get_version, get_compose_env, confirm

PROJROOT = str(Path(__file__).parent)
# PyBuildRoot = PROJROOT.joinpath('build')
# TrackerRoot = PROJROOT.joinpath('facetracker')

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel("DEBUG")


# @task
# def clean(c, docs=False, bytecode=True, extra=""):
#     """[summary]

#     Arguments:
#         c {[type]} -- [description]

#     Keyword Arguments:
#         docs {bool} -- [description] (default: {False})
#         bytecode {bool} -- [description] (default: {True})
#         extra {str} -- [description] (default: {''})
#     """
#     ctx.run("find . -name '*.pyc' -delete")


@task
def clean(ctx, docs=False, bytecode=False, extra=""):
    patterns = []
    if docs:
        patterns.append("docs/_build")
    if bytecode:
        patterns.append("**/*.pyc")
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        ctx.run("find . -name '{}' -delete".format(pattern))


@task
def lint_tests(ctx):
    """
    Check Python code style
    Usage: inv docker.lint-test or inv local.lint-test
    """
    env = get_compose_env(ctx)

    ctx.run(
        f"/usr/local/bin/flake8 --ignore=E501,W503 src/ tasks/ tests/ scripts/ migrations/",
        env=env,
    )


@task
def test(ctx):
    """
    Check Python code style
    Usage: inv docker.test or inv local.test
    """
    env = get_compose_env(ctx)

    ctx.run(
        f"py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=ultron8 tests",
        env=env,
    )


@task
def test_pdb(ctx):
    """
    Check Python code style
    Usage: inv docker.test-pdb or inv local.test-pdb
    """
    env = get_compose_env(ctx)

    ctx.run(
        f"py.test --cov-config .coveragerc --verbose  --pdb --showlocals --cov-report term --cov-report xml --cov=ultron8 tests",
        env=env,
    )


@task
def coverage_run(ctx):
    """
    Check Python code style
    Usage: inv docker.coverage-run or inv local.coverage-run
    """
    env = get_compose_env(ctx)

    ctx.run(
        f"coverage run --source=ultron8/ setup.py tests; coverage report --show-missing; coverage html",
        env=env,
    )


@task
def setup_test(ctx):
    """
    Check Python code style
    Usage: inv docker.setup-test or inv local.setup-test
    """
    env = get_compose_env(ctx)

    ctx.run(f"python setup.py test", env=env)


@task
def run_pytest(ctx):
    """
    Check Python code style
    Usage: inv docker.run-pytest or inv local.run-pytest
    """
    env = get_compose_env(ctx)

    ctx.run(
        f"pytest -s --tb short --cov-config .coveragerc --cov ultron8 tests --cov-report term-missing --cov-report xml:cov.xml --cov-report html:htmlcov --cov-report annotate:cov_annotate",
        env=env,
    )


@task
def serve(ctx):
    """
    Check Python code style
    Usage: inv docker.serve or inv local.serve
    """
    env = get_compose_env(ctx)

    ctx.run(f"bash script/serve", env=env)


@task
def serve_daemon(ctx):
    """
    Check Python code style
    Usage: inv docker.serve-daemon or inv local.serve-daemon
    """
    env = get_compose_env(ctx)

    ctx.run(f"bash script/serve-daemon", env=env)


@task
def backend_pre_start(ctx):
    """
    Check Python code style
    Usage: inv docker.backend-pre-start or inv local.backend-pre-start
    """
    env = get_compose_env(ctx)

    ctx.run(f"python ultron8/api/backend_pre_start.py", env=env)


@task
def initial_data(ctx):
    """
    Check Python code style
    Usage: inv docker.initial-data or inv local.initial-data
    """
    env = get_compose_env(ctx)

    ctx.run(f"python ultron8/initial_data.py", env=env)
