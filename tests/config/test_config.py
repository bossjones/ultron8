"""Test Global Config."""
# pylint: disable=protected-access
import logging
import os
import tempfile
import shutil
from collections import ChainMap
import copy
from copy import deepcopy
import pytest
import pyconfig


import ultron8

# from ultron8.config import do_set_flag
# from ultron8.config import do_get_flag
# from ultron8.config import do_set_multi_flag

# from ultron8.config import ULTRON_CLI_BASE_CONFIG_DIRECTORY
# from ultron8.config import ULTRON_CONFIG_DIRECTORY
# from ultron8.config import ULTRON_CONFIG_PATH
# from ultron8.config import ULTRON_CLUSTERS_PATH
# from ultron8.config import ULTRON_CACHE_PATH
# from ultron8.config import ULTRON_WORKSPACE_PATH
# from ultron8.config import ULTRON_LIBS_PATH
# from ultron8.config import ULTRON_TEMPLATES_PATH

from ultron8 import config
from ultron8.config import get_config

logger = logging.getLogger(__name__)

#############################################
#############################################
#############################################
#############################################


def create_file(path):
    """Create an empty file."""
    with open(path, "w"):
        pass


@pytest.fixture(scope="function")
def fake_dir() -> str:
    base_dir = tempfile.mkdtemp()
    logger.info(f"BASE_DIR: {base_dir}")

    yield base_dir

    # shutil.rmtree(base_dir)


@pytest.fixture(scope="function")
def spoof_config_dir_base_path() -> str:
    base = tempfile.mkdtemp()
    base_dir = tempfile.mkdtemp(prefix="config", dir=base)

    yield base_dir

    shutil.rmtree(base_dir, ignore_errors=True)


@pytest.fixture
def cf():
    return config.get_config()


@pytest.mark.smartonly
@pytest.mark.configonly
@pytest.mark.unittest
class TestSmartConfig:
    def test_is_singleton(self, cf):
        newcf = config.get_config()
        assert id(newcf) == id(cf)

    def test_read_default(self, cf):
        assert cf["flags"]["debug"] == 0
        assert cf["flags"]["verbose"] == 0

    def test_attribute_access(self, cf):
        cf.flags.debug = 1
        assert cf.flags.debug == 1

    def test_str(self, cf):
        cf.flags.debug = 0
        assert (
            "Config(ConfigDict({'clusters_path': 'clusters/', 'cache_path': 'cache/', 'workspace_path': 'workspace/', 'templates_path': 'templates/', 'flags': ConfigDict({'debug': 0, 'verbose': 0, 'keep': 0, 'stderr': 0, 'repeat': 1}), 'clusters': ConfigDict({'instances': ConfigDict({'local': ConfigDict({'url': 'http://localhost:11267', 'token': ''})})})}))"
            in str(cf)
        )

    def test_copy(self, cf):
        cf2 = cf.copy()
        assert cf2 == cf

    def test_config_value_resolution(self, mocker, monkeypatch):
        # create fake config directory
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        full_file_name = "smart.yaml"
        path = os.path.join(fake_dir, full_file_name)

        # create fake fixture data to be returned as list(<fake_dir>)
        default_path = os.path.abspath(os.path.expanduser(fake_dir))
        expected_paths = []
        expected_paths.append(default_path)

        # temporarily patch environment to include fake_dir
        monkeypatch.setenv("ULTRON8DIR", fake_dir)
        # mocker.patch.object(
        #     config, "config_dirs", return_value=expected_paths, autospec=True,
        # )

        # write temporary data to disk
        example_data = """
---
clusters_path: clusters/
cache_path: cache/
workspace_path: workspace/
templates_path: templates/

ultrons:
  - debugultron

async: True

nodes: 0

db_uri: sqlite:///test.db

flags:
    debug: 1
    verbose: 1
    keep: 1
    stderr: 1
    repeat: 0

clusters:
    instances:
        local:
            url: 'http://localhost:11267'
            token: 'memememememememmemememe'
"""

        try:
            with open(path, "wt") as f:
                f.write(example_data)

            config._CONFIG = None
            cf = config.get_config()

            print(cf)

            # verify correct values are being used
            assert cf.clusters.instances.local.token == "memememememememmemememe"
            assert cf.flags.debug == 1
            assert cf.flags.verbose == 1
            assert cf.flags.keep == 1
            assert cf.flags.stderr == 1
            assert cf.flags.repeat == 0

        finally:
            os.unlink(path)
            shutil.rmtree(base, ignore_errors=True)


@pytest.mark.smartonly
@pytest.mark.configonly
@pytest.mark.unittest
class TestSmartConfigErrors:
    def test_attribute_access_keyerror(self):
        config._CONFIG = None
        cf = config.get_config(initdict={"base.tree": "value"})
        assert cf.base.tree == "value"
        cf.base.test = True
        assert cf.base.test == True

        with pytest.raises(AttributeError) as excinfo:
            print(cf.flags.fake)
            assert "Config: No attribute or key " in str(excinfo.value)


@pytest.mark.smartonly
@pytest.mark.configonly
@pytest.mark.unittest
class TestSmartConfigPackageConfig:
    def test_get_package_config(self):
        config._CONFIG = None
        cf = config.get_package_config("ultron8.config")
        assert cf["flags"]["debug"] == 0
        assert cf["flags"]["verbose"] == 0
        assert "flags" in list(cf.keys())
        del cf["flags"]["verbose"]

    def test_delete(self):
        config._CONFIG = None
        cf = config.get_package_config("ultron8.config")
        assert cf["flags"]["debug"] == 0
        assert cf["flags"]["verbose"] == 0
        assert "flags" in list(cf.keys())
        del cf["flags"]["verbose"]


class TestSmartConfigUpdate:
    def test_with_initdict(self):
        config._CONFIG = None
        cf = config.get_config(initdict={"base.tree": "value"})
        assert cf.base.tree == "value"

    # def test_deepcopy(self):
    #     config._CONFIG = None
    #     cf3 = deepcopy(config.get_config(initdict={"base.tree": "value"}))
    #     assert cf3 == config._CONFIG

    def test_get_func(self):
        config._CONFIG = None
        cf = get_config(initdict={"initkey": "initvalue"})
        print(cf)
        # assert str(cf) == "Config(ConfigDict({'clusters_path': 'clusters/', 'cache_path': 'cache/', 'workspace_path': 'workspace/', 'templates_path': 'templates/', 'flags': ConfigDict({'debug': 0, 'verbose': 0, 'keep': 0, 'stderr': 0, 'repeat': 1}), 'clusters': ConfigDict({'instances': ConfigDict({'local': ConfigDict({'url': 'http://localhost:11267', 'token': ''})})}), 'base': ConfigDict({'tree': 'value'})}))"
        # assert str(type(cf)) == "<class 'ultron8.config.Config'>"

        # get_cf_base = cf.get("base")

        assert cf.get("initkey", "") == "initvalue"
        # cf.set("initkey", "newvalue")
        # assert cf.get("initkey", "") == "newvalue"

        # check internal state
        assert cf.maps == [
            config.ConfigDict(
                {
                    "clusters_path": "clusters/",
                    "cache_path": "cache/",
                    "workspace_path": "workspace/",
                    "templates_path": "templates/",
                    "flags": config.ConfigDict(
                        {"debug": 0, "verbose": 0, "keep": 0, "stderr": 0, "repeat": 1}
                    ),
                    "clusters": config.ConfigDict(
                        {
                            "instances": config.ConfigDict(
                                {
                                    "local": config.ConfigDict(
                                        {"url": "http://localhost:11267", "token": ""}
                                    )
                                }
                            )
                        }
                    ),
                    "initkey": "initvalue",
                }
            )
        ]


@pytest.mark.smartonly
@pytest.mark.configonly
@pytest.mark.unittest
class TestSmartConfigDict:
    def test_basics(self):
        config._CONFIG = None
        cf = config.get_config(initdict={"base.foo": "value"})
        cf.base.foo = "foo"
        cf.base.bar = "foo"
        print(cf)

        # check internal state
        assert cf.maps == [
            config.ConfigDict(
                {
                    "clusters_path": "clusters/",
                    "cache_path": "cache/",
                    "workspace_path": "workspace/",
                    "templates_path": "templates/",
                    "flags": config.ConfigDict(
                        {"debug": 0, "verbose": 0, "keep": 0, "stderr": 0, "repeat": 1}
                    ),
                    "clusters": config.ConfigDict(
                        {
                            "instances": config.ConfigDict(
                                {
                                    "local": config.ConfigDict(
                                        {"url": "http://localhost:11267", "token": ""}
                                    )
                                }
                            )
                        }
                    ),
                    "base": config.ConfigDict({"foo": "foo", "bar": "foo"}),
                }
            )
        ]

        # check items/iter/getitem
        assert cf.base.items() == dict(foo="foo", bar="foo").items()

        # check len
        assert len(cf.base) == 2

        # check contains
        for key in ["foo", "bar"]:
            assert key in cf.base

        # check get
        d = cf.base
        cf.base.z = 100
        for k, v in dict(foo="foo", bar="foo", z=100).items():
            assert cf.base.get(k, 100) == v

        # Test proper exception thrown when trying to access attribute that doesn't exist
        with pytest.raises(
            AttributeError
        ) as excinfo:  # pylint: disable=pointless-statement
            cf.base.gg
        assert "No attribute or key 'gg'" in str(excinfo.value)

        # unmask a value
        del cf["base"]["z"]

        # check internal state
        assert cf.maps == [
            config.ConfigDict(
                {
                    "clusters_path": "clusters/",
                    "cache_path": "cache/",
                    "workspace_path": "workspace/",
                    "templates_path": "templates/",
                    "flags": config.ConfigDict(
                        {"debug": 0, "verbose": 0, "keep": 0, "stderr": 0, "repeat": 1}
                    ),
                    "clusters": config.ConfigDict(
                        {
                            "instances": config.ConfigDict(
                                {
                                    "local": config.ConfigDict(
                                        {"url": "http://localhost:11267", "token": ""}
                                    )
                                }
                            )
                        }
                    ),
                    "base": config.ConfigDict({"foo": "foo", "bar": "foo"}),
                }
            )
        ]

        # check items/iter/getitem
        assert d.items() == dict(foo="foo", bar="foo").items()

        # check len
        assert len(d) == 2

        # check contains
        for key in ["foo", "bar"]:
            assert key in d

        # check repr
        assert repr(d) == type(d).__name__ + "({'foo': 'foo', 'bar': 'foo'})"

        # check shallow copies
        for e in cf.copy(), copy.copy(cf):
            assert cf == e
            assert cf.maps == e.maps
            for m1, m2 in zip(cf.maps[1:], e.maps[1:]):
                assert m1 == m2


@pytest.mark.smartonly
@pytest.mark.configonly
@pytest.mark.unittest
class TestConfigManager:
    def test_basics(self, mocker, monkeypatch):
        # create fake config directory
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        full_file_name = "smart.yaml"
        path = os.path.join(fake_dir, full_file_name)

        # create fake fixture data to be returned as list(<fake_dir>)
        default_path = os.path.abspath(os.path.expanduser(fake_dir))
        expected_paths = []
        expected_paths.append(default_path)

        # temporarily patch environment to include fake_dir
        monkeypatch.setenv("ULTRON8DIR", fake_dir)

        # write temporary data to disk
        example_data = """
---
clusters_path: clusters/
cache_path: cache/
workspace_path: workspace/
templates_path: templates/

flags:
    debug: 1
    verbose: 1
    keep: 1
    stderr: 1
    repeat: 0

clusters:
    instances:
        local:
            url: 'http://localhost:11267'
            token: 'memememememememmemememe'
"""

        try:
            with open(path, "wt") as f:
                f.write(example_data)

            config._CONFIG = None
            cm = config.ConfigManager()

            print(cm)

            # verify we can access the data object
            assert cm.data.clusters.instances.local.token == "memememememememmemememe"
            assert cm.data.flags.debug == 1
            assert cm.data.flags.verbose == 1
            assert cm.data.flags.keep == 1
            assert cm.data.flags.stderr == 1
            assert cm.data.flags.repeat == 0

            # verify we can access the config api as well
            assert cm.api._env_var == "ULTRON8DIR"

            assert (
                cm.get_config_dir() == fake_dir
            )  # eg. /Users/bossjones/.config/ultron8
            assert (
                cm.get_filename() == "smart.yaml"
            )  # eg. /Users/bossjones/.config/ultron8
            assert str(repr(cm)) == "<{}: {}/{}>".format(
                cm.__class__.__name__, cm.get_config_dir(), cm.get_filename()
            )

            # test saving data
            cm.data["bossjones"] = 1911
            cm.save()

            # read from disk again
            cm.api.read()

            assert cm.data.bossjones == 1911

        finally:
            os.unlink(path)
            shutil.rmtree(base, ignore_errors=True)


#############################################
#############################################
#############################################

# FIXME:
# FIXME:
# FIXME:
# FIXME:
# # INFO: https://stackoverflow.com/questions/41274325/why-does-monkeypatching-os-path-require-a-path-argument
# @pytest.mark.configonly
# @pytest.mark.unittest
# class TestConfigConstants:
#     def test_ultron_config_path(self, mocker, monkeypatch, fake_dir) -> None:
#         def mockreturn(path):
#             return fake_dir
#         # Application of the monkeypatch to replace Path.home
#         # with the behavior of mockreturn defined above.
#         # monkeypatch.setattr(ultron8.config.os.path, 'expanduser', mockreturn)
#         # monkeypatch.setattr(ultron8.config, 'ULTRON_CLI_BASE_CONFIG_DIRECTORY', fake_dir)
#         # import pdb; pdb.set_trace()

#         temp_config_cidr = mockreturn(fake_dir)
#         mocker.patch("ultron8.config.ULTRON_CLI_BASE_CONFIG_DIRECTORY", temp_config_cidr)

#         assert ULTRON_CONFIG_DIRECTORY == f"{temp_config_cidr}"
#         # assert ULTRON_CONFIG_PATH == f"{temp_config_cidr}/config.json"


# def _fake_config(override=None):
#         """Create a temporary config file."""
#         base = tempfile.mkdtemp()
#         logger.debug("base tempfile: {}".format(base))
#         config_file = os.path.join(base, "config.yaml")

#         #############################################################
#         # Example of config_file:
#         #############################################################
#         #  ⌁ pi@scarlett-ansible-manual1604-2  ~  ll /tmp/tmpnxz2wsa2
#         # total 12
#         # drwx------  2 pi   pi   4096 Feb 24 15:58 ./
#         # drwxrwxrwt 15 root root 4096 Feb 24 15:58 ../
#         # -rw-rw-r--  1 pi   pi   1034 Feb 24 15:58 config.yaml
#         # ⌁ pi@scarlett-ansible-manual1604-2  ~
#         #############################################################

#         if override is not None:
#             with open(config_file, "wt") as f:
#                 f.write(override)
#             return base, config_file

#         with open(config_file, "wt") as f:
#             f.write(DEFAULT_CONFIG)

#         return base, config_file

#     fake_config_file_path_base, fake_config_file_path = _fake_config(
#         override=RUSSIAN_CONFIG
#     )
