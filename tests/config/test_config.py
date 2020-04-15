"""Test Global Config."""
# pylint: disable=protected-access
import logging
import os
import tempfile
import shutil
from collections import ChainMap
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

    # def test_config_type(self, cf):
    #     assert type(cf) == ChainMap
    # <class 'ultron8.config.Config'>


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
