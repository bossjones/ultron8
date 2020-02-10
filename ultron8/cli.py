from typing import Any
from typing import Tuple

import json
import os
import sys
import shutil
import codecs

# import pdb
import click
import pyconfig

from .logging_init import getLogger
from .process import fail

logger = getLogger(__name__)

stdin, stdout = sys.stdin, sys.stdout

CONTEXT_SETTINGS = dict(auto_envvar_prefix="ULTRON8_CLI")


def set_trace():
    """[Use this to set pdb trace for debugging]
    """
    # SOURCE: https://github.com/pallets/click/issues/1121
    # pdb.Pdb(stdin=stdin, stdout=stdout).set_trace()
    pass


# http://click.palletsprojects.com/en/5.x/options/
# http://click.palletsprojects.com/en/5.x/complex/#complex-guide
# http://click.palletsprojects.com/en/5.x/commands/
# https://github.com/pallets/click/blob/master/examples/complex/complex/cli.py


def write_file(file_path, contents, mode="w"):
    with open(file_path, mode, encoding="utf-8") as file_handle:
        file_handle.write(contents)


def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file_handle:
        content = file_handle.read().replace("\n", "")
    return json.loads(content)


def write_json_file(file_path, data):
    write_file(file_path, json.dumps(data))


class NullConfig(object):
    def __getattr__(self, name):
        return self

    def __call__(self):
        return None

    def exists(self):
        return False


class ConfigManager(object):
    def __init__(self, data):
        self.__data = data

    def __getattr__(self, name):
        if name in self.__data:
            return ConfigManager(self.__data[name])
        return NullConfig()

    def __call__(self):
        return self.__data

    def exists(self):
        return True


def app_home():
    try:
        return os.path.join(os.environ["HOME"], ".ultron8")
    except KeyError:
        raise "HOME environment variable not set?"


def mkdir_if_dne(target):
    if not os.path.isdir(target):
        os.makedirs(target)


def prep_default_config():
    home = app_home()
    if not os.path.exists(home):
        os.makedirs(home)
    default_cfg = os.path.join(home, "config.json")
    if not os.path.exists(default_cfg):
        file = open(default_cfg, "w")
        file.write("{}")
        file.close()
    return default_cfg


class Workspace:
    def __init__(self, wdir=None, libdir=None):
        self._wdir = None
        if wdir is None:
            wdir = self._default_workspace()
        self.set_dir(wdir)
        self._lib_dir = None
        if libdir is None:
            libdir = self._default_libdir()
        mkdir_if_dne(libdir)
        self._lib_dir = libdir

    def clean(self):
        shutil.rmtree(self._wdir)
        self.set_dir(self._wdir)

    def set_dir(self, d):
        """
        Sets the directory that this object is tied to. If the
        directory given actually is different, the contents will be
        copied over
        """
        mkdir_if_dne(d)
        old_workspace = self._wdir
        self._wdir = d
        if not d == old_workspace and old_workspace is not None:
            self.copy_contents(old_workspace)

    def copy_libs(self):
        self.copy_contents(self._lib_dir, subdir=os.path.join("templates", "libs"))

    def copy_templates(self, in_dir):
        """
        copy over lib files, and THEN user files to ensure overwrites
        """
        self.copy_contents(in_dir, subdir="templates")

    def copy_contents(self, source, subdir="", sourcedir=None):
        if sourcedir is None:
            sourcedir = self._wdir
        subdir_fp = os.path.join(sourcedir, subdir)
        mkdir_if_dne(subdir_fp)
        if os.path.isfile(source) and not os.path.isdir(source):
            shutil.copy(source, subdir_fp)
            return
        # because shutil.copytree fails when sourcedir exists and
        # is given as the destination
        for fi in os.listdir(source):
            fpath = os.path.join(source, fi)
            # listed dir IS the target dir - skip to prevent infinite recursion
            if fpath in os.path.join(sourcedir, fi):
                continue
            if os.path.isdir(fpath):
                shutil.copytree(fpath, os.path.join(subdir_fp, fi))
                continue
            shutil.copy(fpath, subdir_fp)

    def create_subdir(self, subdir):
        full_path = os.path.join(self._wdir, subdir)
        if os.path.isdir(full_path):
            return
        os.mkdir(full_path)

    def write_template(self, path, contents):
        write_file(os.path.join(self._wdir, path), contents, mode="a")

    def template_subdir(self):
        return os.path.join(self._wdir, "templates")

    def _default_workspace(self):
        return os.path.join(app_home(), "workspace")

    def _default_libdir(self):
        return os.path.join(app_home(), "libs")


class Environment(object):
    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


DEFAULT_CONFIG = """
clusters:
    instances:
        local:
            url: "http://localhost:11267"
            token: ""
"""


pass_environment = click.make_pass_decorator(Environment, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))


def _info() -> None:
    """Get Info on Ultron"""
    logger.info("Ultron8 is running")


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option("--working-dir", envvar="ULTRON_WORKING_DIR", default="working_dir")
@click.option("--config-dir", envvar="ULTRON_CONFIG_DIR", default=".config")
@click.option("--debug", is_flag=True, envvar="ULTRON_DEBUG")
@click.option("-v", "--verbose", count=True, help="Enables verbose mode.")
@click.pass_context
def cli(ctx, working_dir: str, config_dir: str, debug: bool, verbose: int):
    """
    Ultronctl - Client Side CLI tool to manage an Ultron8 Cluster.
    """
    # SOURCE: http://click.palletsprojects.com/en/7.x/commands/?highlight=__main__
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below
    ctx.ensure_object(dict)

    set_flag("working-dir", working_dir)
    set_flag("config-dir", config_dir)
    set_flag("debug", debug)
    set_flag("verbose", verbose)

    ctx.obj["working_dir"] = working_dir
    ctx.obj["config_dir"] = config_dir
    ctx.obj["debug"] = debug
    ctx.obj["cfg_file"] = prep_default_config()
    ctx.obj["verbose"] = verbose
    ctx.obj["workspace"] = Workspace()
    ctx.obj["configmanager"] = ConfigManager(load_json_file(ctx.obj["cfg_file"]))


# SOURCE: https://kite.com/blog/python/python-command-line-click-tutorial/


@cli.command()
@click.pass_context
def dummy(ctx):
    """
    Dummy command, doesn't do anything.
    """
    if get_flag("debug"):
        click.echo("Debug mode initiated")
        set_trace()

    if get_flag("debug"):
        click.echo("[DUMP ctx]: ")
        for k, v in ctx.obj.items():
            click.echo(f"  {k} -> {v}")

    click.echo("Dummy command, doesn't do anything.")

    click.echo("Ran [{}]| test".format(sys._getframe().f_code.co_name))


@cli.command()
@click.option("--fact", multiple=True, help="Set a fact, like --fact=color:blue.")
@click.pass_context
def info(ctx, fact: Tuple[str]):
    """Get info on running Ultron8 process."""
    if get_flag("debug"):
        click.echo("Debug mode initiated")
        set_trace()

    logger.debug("info subcommand called from cli")
    set_fact_flags(fact)
    _info()


# @cli.command()
# @click.option('--clean-assets', is_flag=True, help='Also remove assets.')
# def clean(clean_assets: bool):
#     """Remove rendered files and downloaded assets."""
#     logger.debug('clean subcommand called from cli')
#     set_flag('clean-assets', clean_assets)
#     commands.clean()


# @cli.command()
# @click.option('--clean-assets', is_flag=True, help='Reaquire assets.')
# @click.option('--asset-set', default='default', help='Specify the asset set to build with.')
# @click.option('--fact', multiple=True, help='Set a fact, like --fact=color:blue.')
# def build(clean_assets: bool, asset_set: str, fact: Tuple[str]):
#     """Build images."""
#     logger.debug('build subcommand called from cli')
#     set_flag('asset-set', asset_set)
#     set_flag('clean-assets', clean_assets)
#     set_fact_flags(fact)
#     # FIXME: Should we auto-clean assets if the assetset changes?
#     commands.clean()
#     commands.acquire()
#     commands.render()
#     commands.build()


# @cli.command()
# @click.option('--asset-set', default='default', help='Specify the asset set to acquire.')
# @click.option('--fact', multiple=True, help='Set a fact, like --fact=color:blue.')
# def acquire(asset_set: str, fact: Tuple[str]):
#     """Acquire assets."""
#     logger.debug('acquire subcommand called from cli')
#     set_flag('asset-set', asset_set)
#     set_fact_flags(fact)

#     # Since the user explicitly called "acquire", make sure they get fresh assets
#     # by cleaning the assets dir first.
#     set_flag('clean-assets', True)
#     commands.clean()

#     commands.acquire()

# @cli.command()
# @click.option('--asset-set', default='default', help='Specify the asset set to acquire.')
# @click.option('--fact', multiple=True, help='Set a fact, like --fact=color:blue.')
# def acquire(asset_set: str, fact: Tuple[str]):
#     """Acquire assets."""
#     logger.debug('acquire subcommand called from cli')
#     set_flag('asset-set', asset_set)
#     set_fact_flags(fact)

#     # Since the user explicitly called "acquire", make sure they get fresh assets
#     # by cleaning the assets dir first.
#     set_flag('clean-assets', True)
#     commands.clean()

#     commands.acquire()


def set_flag(flag: str, value: Any) -> None:
    """Store a CLI flag in the config as "cli.flags.FLAG"."""
    pyconfig.set(f"cli.flags.{flag}", value)


def get_flag(flag: str, default: Any = None) -> Any:
    """Get a CLI flag from the config."""
    return pyconfig.get(f"cli.flags.{flag}", default)


def set_fact_flags(flag_args: Tuple[str]) -> None:
    """Take "--fact" flags from the CLI and store them in the config as a dict."""
    facts = {}

    for arg in flag_args:
        if ":" not in arg:
            logger.critical('Arguments to "--fact" must be colon seperated.')
            logger.critical('Like: "ultronctl --fact=temperature:hot')
            fail()
        fact, value = arg.split(":", 1)
        logger.debug(f'Setting fact from cli: "{fact}" -> "{value}"')
        facts[fact] = value

    set_flag("fact", facts)


# import logging
# import random
# import string

# import requests

# from ultron8.api import settings

# from typing import Dict

# logger = logging.getLogger(__name__)


# def random_lower_string() -> str:
#     return "".join(random.choices(string.ascii_lowercase, k=32))


# def get_server_api() -> str:
#     server_name = f"http://{settings.SERVER_NAME}"
#     logger.debug("server_name: '%s'", server_name)
#     return server_name


# def get_superuser_token_headers() -> Dict[str, str]:
#     server_api = get_server_api()
#     login_data = {
#         "username": settings.FIRST_SUPERUSER,
#         "password": settings.FIRST_SUPERUSER_PASSWORD,
#     }
#     r = requests.post(
#         f"{server_api}{settings.API_V1_STR}/login/access-token", data=login_data
#     )
#     tokens = r.json()
#     a_token = tokens["access_token"]
#     headers = {"Authorization": f"Bearer {a_token}"}
#     # superuser_token_headers = headers
#     return headers

# if __name__ == '__main__':
#     cli()

# if __name__ == '__main__':
#     print(sys.argv[1:])
#     runner = CliRunner()
#     print(runner.invoke(cli))


@cli.command()
@click.pass_context
def login(ctx):
    """
    Login CLI. Used to interact with ultron8 api.
    """
    if get_flag("debug"):
        click.echo("Debug mode initiated")
        set_trace()

    click.echo("BLAH")


@cli.command()
@click.option(
    "-m",
    "--method",
    type=click.Choice(["GET", "POST", "PUT", "DELETE"], case_sensitive=False),
)
@click.pass_context
def user(ctx, method):
    """
    User CLI. Used to interact with ultron8 api.
    """
    if get_flag("debug"):
        click.echo("Debug mode initiated")
        set_trace()

    click.echo("BLAH")


if __name__ == "__main__":
    # print(sys.argv[1:])
    # runner = CliRunner()
    # print(runner.invoke(cli, args=sys.argv[1:]))
    # pylint: disable=no-value-for-parameter
    cli(sys.argv[1:])
