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


@task(incrementable=["verbose"])
def coverage_clean(ctx, loc="local", verbose=0, cleanup=False):
    """
    clean coverage files
    Usage: inv ci.coverage-clean
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
rm -rf htmlcov/*
rm -rf cov_annotate/*
rm -f cov.xml
    """

    if verbose >= 1:
        msg = "{}".format(_cmd)
        click.secho(msg, fg=COLOR_SUCCESS)

    ctx.run(_cmd)


@task
def pylint(ctx, loc="local", tests=False, everything=False, specific=""):
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

    if tests:
        ctx.run(
            "pylint --disable=all --enable=F,E --rcfile ./lint-configs-python/python/pylintrc tests"
        )
    elif everything:
        ctx.run("pylint --rcfile ./lint-configs-python/python/pylintrc tests ultron8")
    elif specific:
        ctx.run(
            f"pylint --disable=all --enable={specific} --rcfile ./lint-configs-python/python/pylintrc tests ultron8"
        )
    else:
        ctx.run(
            "pylint --disable=all --enable=F,E --rcfile ./lint-configs-python/python/pylintrc ultron8"
        )


@task(incrementable=["verbose"])
def mypy(ctx, loc="local", verbose=0):
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


@task(incrementable=["verbose"])
def isort(
    ctx, loc="local", check=False, dry_run=False, verbose=0, apply=False, diff=False
):
    """
    isort ultron8 module. Some of the arguments were taken from the starlette contrib scripts. Tries to align w/ black to prevent having to reformat multiple times.

    To check mode only(does not make changes permenantly):
        Usage: inv ci.isort --check -vvv
    Simply display command we would run:
        Usage: inv ci.isort --check --dry-run -vvv
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = "isort --recursive"

    if check:
        _cmd += " --check-only"

    if diff:
        _cmd += " --diff"

    if verbose >= 2:
        _cmd += " --verbose"

    if apply:
        _cmd += " --apply"

    _cmd += " ultron8 tests"

    if verbose >= 1:
        msg = "{}".format(_cmd)
        click.secho(msg, fg=COLOR_SUCCESS)

    if dry_run:
        click.secho(
            "[isort] DRY RUN mode enabled, not executing command: {}".format(_cmd),
            fg=COLOR_CAUTION,
        )
    else:
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
    fastapionly=False,
    jwtonly=False,
    mockedfs=False,
    clionly=False,
    usersonly=False,
    convertingtotestclientstarlette=False,
    loggeronly=False,
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

    if fastapionly:
        _cmd += r" -m fastapionly "

    if jwtonly:
        _cmd += r" -m jwtonly "

    if mockedfs:
        _cmd += r" -m mockedfs "

    if clionly:
        _cmd += r" -m clionly "

    if usersonly:
        _cmd += r" -m usersonly "

    if convertingtotestclientstarlette:
        _cmd += r" -m convertingtotestclientstarlette "

    if loggeronly:
        _cmd += r" -m loggeronly "

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


@task(
    incrementable=["verbose"],
    pre=[call(view_api_docs, loc="local"), call(view_coverage, loc="local"),],
)
def browser(ctx, loc="local"):
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

    msg = "Finished loading everything into browser"
    click.secho(msg, fg=COLOR_SUCCESS)


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
    ],
    incrementable=["verbose"],
)
def monkeytype(
    ctx,
    loc="local",
    verbose=0,
    cleanup=False,
    test=False,
    apply=False,
    stub=False,
    dry_run=False,
):
    """
    Use monkeytype to collect runtime types of function arguments and return values, and automatically generate stub files
    or even add draft type annotations directly to python code. Uses pytest to access all lines of code that have testing setup.

    To generate stubs:
        Usage: inv ci.monkeytype --test -vvv
    To apply stubs to existing code base:
        Usage: inv ci.monkeytype --test --apply --stub -vvv
    To apply stubs to existing code base(dry run):
        Usage: inv ci.monkeytype --test --apply --stub -vvv --dry-run
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    # NOTE: https://monkeytype.readthedocs.io/en/stable/faq.html#why-did-my-test-coverage-measurement-stop-working
    _cmd = r"""monkeytype run "`command -v pytest`" --no-cov --verbose --mypy --showlocals --tb=short tests"""

    if test:
        if verbose >= 1:
            msg = "{}".format(_cmd)
            click.secho(msg, fg=COLOR_SUCCESS)

        if dry_run:
            click.secho(
                "[monkeytype] DRY RUN mode enabled, not executing command: {}".format(
                    _cmd
                ),
                fg=COLOR_CAUTION,
            )
        else:
            ctx.run(_cmd)

    _cmd_stub = r"""
modules_array=()
while IFS= read -r line; do
    modules_array+=( "$line" )
done < <( monkeytype list-modules | grep -v "pytestipdb" )

echo "Stub all modules using monkeytype"
for element in "${modules_array[@]}"
do
    filename=$(echo $element | sed 's,\.,\/,g')
    _basedir=$(dirname "$filename")
    mkdir -p stubs/$_basedir || true
    touch stubs/$_basedir/__init__.pyi
    echo " [run] monkeytype stub ${element} > stubs/$filename.pyi"
    monkeytype -v stub ${element} > stubs/$filename.pyi
done

    """

    if stub:
        if dry_run:
            click.secho(
                "[monkeytype] DRY RUN mode enabled, not executing command: \n\n{}".format(
                    _cmd_stub
                ),
                fg=COLOR_CAUTION,
            )
        else:
            ctx.run(_cmd_stub)

    _cmd_apply = r"""
modules_array=()
while IFS= read -r line; do
    modules_array+=( "$line" )
done < <( monkeytype list-modules | grep -v "pytestipdb" )

echo "apply all modules using monkeytype"
for element in "${modules_array[@]}"
do
    monkeytype apply ${element}
done
    """
    #     _cmd_apply = r"""
    # find stubs -type f -name '*.pyi' ! -name '*.venv' -print0 | xargs -I FILE -t -0 -n1 monkeytype -v apply FILE
    #     """

    # find stubs -type f -name '*.pyi' ! -name '*.venv' -print0 | xargs -I FILE -t -0 -n1 monkeytype -v apply FILE

    if apply:
        if dry_run:
            click.secho(
                "[monkeytype] DRY RUN mode enabled, not executing command: \n\n{}".format(
                    _cmd_apply
                ),
                fg=COLOR_CAUTION,
            )
        else:
            ctx.run(_cmd_apply)


def autoflake(
    ctx, loc="local", verbose=0, check=False, dry_run=False,
):
    """
    Use autoflake to remove unused imports, recursively, remove unused variables, and exclude __init__.py

    To run autoflake in check only mode:
        Usage: inv ci.autoflake --check -vvv
    To run autoflake in check only mode(dry-run):
        Usage: inv ci.autoflake --check -vvv --dry-run
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = "autoflake"
    _cmd += " --remove-all-unused-imports --recursive --remove-unused-variables"

    if check:
        _cmd += " --check"

    _cmd += " ultron8"
    _cmd += " --exclude=__init__.py"

    if verbose >= 1:
        msg = "{}".format(_cmd)
        click.secho(msg, fg=COLOR_SUCCESS)

    if dry_run:
        click.secho(
            "[autoflake] DRY RUN mode enabled, not executing command: {}".format(_cmd),
            fg=COLOR_CAUTION,
        )
    else:
        ctx.run(_cmd)


@task(
    pre=[call(clean, loc="local"), call(verify_python_version, loc="local"),],
    incrementable=["verbose"],
    aliases=["clean_stubs", "clean_monkeytype"],
)
def clean_pyi(ctx, loc="local", verbose=0, dry_run=False):
    """
    Clean all stub files

    To clean stubs:
        Usage: inv ci.clean-pyi -vvv
    To clean stubs(dry run):
        Usage: inv ci.clean-pyi -vvv --dry-run
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    # NOTE: https://monkeytype.readthedocs.io/en/stable/faq.html#why-did-my-test-coverage-measurement-stop-working
    _cmd = r"""find . -name '*.pyi' -exec rm -fv {} +"""

    if verbose >= 1:
        msg = "{}".format(_cmd)
        click.secho(msg, fg=COLOR_SUCCESS)

    if dry_run:
        click.secho(
            "[monkeytype] DRY RUN mode enabled, not executing command: {}".format(_cmd),
            fg=COLOR_CAUTION,
        )
    else:
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
        # call(pytest, loc="local", fastapionly=True),
        # call(pytest, loc="local", jwtonly=True),
        # call(pytest, loc="local", mockedfs=True),
        # call(pytest, loc="local", clionly=True),
        # call(pytest, loc="local", usersonly=True),
        # call(pytest, loc="local", convertingtotestclientstarlette=True),
        # call(pytest, loc="local", loggeronly=True),
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
