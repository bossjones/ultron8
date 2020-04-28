"""
ci tasks
"""
import os
import logging
from invoke import task, call
import click
from tasks.utils import get_compose_env

# from tasks.core import clean, execute_sql

from .utils import (
    COLOR_WARNING,
    COLOR_DANGER,
    COLOR_SUCCESS,
    COLOR_CAUTION,
    COLOR_STABLE,
)

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


@task(incrementable=["verbose"])
def clean(ctx, loc="local", verbose=0, cleanup=False):
    """
    clean compiled python artifacts
    Usage: inv ci.clean
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = r"""
find . -name '*.pyc' -exec rm -fv {} +
find . -name '*.pyo' -exec rm -fv {} +
find . -name '__pycache__' -exec rm -frv {} +
rm -f .coverage
    """

    if verbose >= 1:
        msg = "{}".format(_cmd)
        click.secho(msg, fg=COLOR_SUCCESS)

    ctx.run(_cmd)


@task
def pylint(ctx, loc="local"):
    """
    pylint ultron8 folder
    Usage: inv ci.pylint
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    ctx.run(
        "pylint --disable=all --enable=F,E --rcfile ./lint-configs-python/python/pylintrc ultron8"
    )


@task
def mypy(ctx, loc="local"):
    """
    mypy ultron8 folder
    Usage: inv ci.mypy
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    ctx.run("mypy --config-file ./lint-configs-python/python/mypy.ini ultron8 tests")


@task(incrementable=["verbose"])
def black(ctx, loc="local", check=True, debug=False, verbose=0):
    """
    Run black code formatter
    Usage: inv ci.black
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _black_excludes = r"/(\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|_build|buck-out|dist|ultron8_venv*)/"
    _cmd = ""

    if check:
        _cmd = "black --check --exclude=ultron8_venv* --verbose ultron8"
    else:
        if verbose >= 1:
            msg = "[black] check mode disabled"
            click.secho(msg, fg="green")
        _cmd = r"black --exclude='{}' --verbose ultron8".format(_black_excludes)

    ctx.run(_cmd)


@task
def isort(ctx, loc="local", check=True, debug=False):
    """
    isort ultron8 module
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = ""

    if check:
        _cmd = "isort --recursive --check-only --diff --verbose ultron8 tests"
    else:
        _cmd = "isort --recursive --diff --verbose ultron8 tests"

    ctx.run(_cmd)


@task
def verify_python_version(ctx, loc="local", check=True, debug=False):
    """
    verify_python_version is 3.7.4
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    # Python 3.7.4
    res = ctx.run("python --version")

    assert "Python 3.7.4" in res.stdout.rstrip()


@task
def pre_start(ctx, loc="local", check=True, debug=False):
    """
    pre_start ultron8 module
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    ctx.run("python ultron8/api/tests_pre_start.py")


@task(incrementable=["verbose"])
def pytest(
    ctx,
    loc="local",
    check=True,
    debug=False,
    verbose=0,
    pdb=False,
    configonly=False,
    settingsonly=False,
    pathsonly=False,
    workspaceonly=False,
    clientonly=False,
):
    """
    Run pytest
    Usage: inv ci.pytest
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = r"py.test"

    if verbose >= 1:
        msg = "[pytest] check mode disabled"
        click.secho(msg, fg="green")
        _cmd += r" --verbose "

    if configonly:
        _cmd += r" -m configonly "

    if pathsonly:
        _cmd += r" -m pathsonly "

    if settingsonly:
        _cmd += r" -m settingsonly "

    if workspaceonly:
        _cmd += r" -m workspaceonly "

    if clientonly:
        _cmd += r" -m clientonly "

    if pdb:
        _cmd += r" --pdb "

    _cmd += r" --cov-config=setup.cfg --verbose --cov-append --cov-report=term-missing --cov-report=xml:cov.xml --cov-report=html:htmlcov --cov-report=annotate:cov_annotate --mypy --showlocals --tb=short --cov=ultron8 tests"

    ctx.run(_cmd)


@task(incrementable=["verbose"])
def view_coverage(ctx, loc="local"):
    """
    Open coverage report inside of browser
    Usage: inv ci.view-coverage
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = r"./script/open-browser.py file://${PWD}/htmlcov/index.html"

    ctx.run(_cmd)


@task(
    incrementable=["verbose"],
    aliases=["swagger", "openapi", "view_openapi", "view_swagger"],
)
def view_api_docs(ctx, loc="local"):
    """
    Open api swagger docs inside of browser
    Usage: inv ci.view-api-docs
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = r"./script/open-browser.py http://localhost:11267/docs"

    ctx.run(_cmd)


@task(incrementable=["verbose"])
def alembic_upgrade(ctx, loc="local"):
    """
    Run alembic upgrade head
    Usage: inv ci.alembic-upgrade
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = r"alembic upgrade head"

    ctx.run(_cmd)


@task(incrementable=["verbose"])
def editable(ctx, loc="local"):
    """
    Run: pip install -e .
    Usage: inv ci.editable
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = r"pip install -e ."

    ctx.run(_cmd)


@task(
    pre=[
        call(clean, loc="local"),
        call(verify_python_version, loc="local"),
        call(pre_start, loc="local"),
        call(alembic_upgrade, loc="local"),
        # call(pytest, loc="local", configonly=True),
        # call(pytest, loc="local", settingsonly=True),
        # call(pytest, loc="local", pathsonly=True),
        # call(pytest, loc="local", workspaceonly=True),
        # call(pytest, loc="local", clientonly=True),
        call(pytest, loc="local"),
    ],
    incrementable=["verbose"],
)
def travis(ctx, loc="local", check=True, debug=False, verbose=0):
    """
    Run travis
    Usage: inv ci.travis
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    if verbose >= 1:
        msg = "[travis] check mode disabled"
        click.secho(msg, fg="green")
    _cmd = r"""
mv -f .coverage .coverage.tests || true
coverage combine
"""

    ctx.run(_cmd)
