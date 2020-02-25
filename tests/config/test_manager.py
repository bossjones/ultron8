"""Test config utils."""
# pylint: disable=protected-access
import logging
import os
import shutil
import tempfile
import unittest
import unittest.mock as mock
from pathlib import Path
from tempfile import mkdtemp
from tempfile import NamedTemporaryFile

import pytest

import ultron8.config
from tests import helper
from ultron8.yaml import yaml
from ultron8.yaml import yaml_load
from ultron8.yaml import yaml_save

from ultron8.config.manager import NullConfig
from ultron8.config.manager import ConfigProxy

# from . import helper
# import helper


@pytest.fixture(scope="class")
def get_fake_config_proxy():
    config_proxy = ConfigProxy({"foo": "bar"})
    return config_proxy


@pytest.mark.configonly
@pytest.mark.unittest
class TestNullConfig:
    def test_NullConfig_getattr_returns_self_test(self) -> None:
        cfg = NullConfig()
        assert cfg == cfg.nested_thing

    def test_NullConfig_call_returns_none_test(self) -> None:
        assert NullConfig().thing() is None

    def test_NullConfig_nothing_exists_test(self) -> None:
        assert NullConfig().thing.exists() is False


@pytest.mark.configonly
@pytest.mark.unittest
class TestConfigProxy:
    def test_ConfigProxy_existing_k_returns_config(self, get_fake_config_proxy):
        assert type(get_fake_config_proxy.foo) is ConfigProxy

    def test_ConfigProxy_non_existing_k_returns_null_config(
        self, get_fake_config_proxy
    ):
        assert type(get_fake_config_proxy.baz) is NullConfig

    def test_ConfigProxy_kv_get_on_k_returns_v(self, get_fake_config_proxy):
        assert get_fake_config_proxy.foo() == "bar"

    def test_ConfigProxy_kv_get_on_nonexistant_k_returns_none(
        self, get_fake_config_proxy
    ):
        assert get_fake_config_proxy.baz() is None

    def test_ConfigProxy_real_kv_exist_returns_true(self, get_fake_config_proxy):
        assert get_fake_config_proxy.foo.exists()

    def test_ConfigProxy_bad_kv_exist_returns_false(self, get_fake_config_proxy):
        assert get_fake_config_proxy.baz.exists() is False


# def create_file(path):
#     """Create an empty file."""
#     with open(path, "w"):
#         pass


# @pytest.fixture(scope="function")
# def get_fake_config_path():
#     base = tempfile.mkdtemp()
#     config_dir = tempfile.mkdtemp(prefix="config", dir=base)
#     yield base, config_dir

#     # config_file = os.path.join(config_dir, "config.yaml")


# def create_subdir(path):
#     p = Path(path)
#     p.mkdir(parents=True, exist_ok=True)
#     assert p.is_dir()


# @pytest.fixture(scope="function")
# def get_fake_moonbeam_service_config_path():
#     base = tempfile.mkdtemp()
#     share_dir = tempfile.mkdtemp(prefix="share", dir=base)
#     path_to_v1_dir = os.path.join(share_dir, "v1")
#     path_to_v2_dir = os.path.join(share_dir, "v2")
#     # Now create a v1/v2 folder
#     create_subdir(path_to_v1_dir)
#     create_subdir(path_to_v2_dir)
#     # v1_dir = tempfile.mkdtemp(prefix='v1', dir=share_dir)
#     # v2_dir = tempfile.mkdtemp(prefix='v2', dir=share_dir)
#     yield base, share_dir, path_to_v1_dir, path_to_v2_dir

#     shutil.rmtree(base)

#     # share_file = os.path.join(v1_dir, "config.yaml")


# @pytest.fixture(scope="function")
# def fake_moonbeam_service_config(get_fake_moonbeam_service_config_path):
#     """Create a temporary moonbeam service config file."""
#     # base, share_dir, path_to_v1_dir, path_to_v2_dir = get_fake_moonbeam_service_config_path
#     _, share_dir, _, path_to_v2_dir = get_fake_moonbeam_service_config_path

#     # ------------------------------------------------
#     # Get fixture data from disk
#     # ------------------------------------------------
#     example_data_file = "fake_moonbeam_app_code_deploy_service"
#     example_data = helper.example_data_to_str(example_data_file)
#     # ------------------------------------------------

#     # base = tempfile.mkdtemp()
#     # config_dir = tempfile.mkdtemp(prefix='config', dir=base)
#     full_file_name = "{}.yaml".format(example_data_file)
#     config_file = os.path.join(path_to_v2_dir, full_file_name)

#     with open(config_file, "wt") as f:
#         f.write(example_data)

#     temp_config = yaml_load(config_file)

#     yield share_dir, config_file, temp_config

#     os.unlink(config_file)


# @pytest.fixture(scope="function")
# def fake_config():
#     """Create a temporary config file."""

#     # ------------------------------------------------
#     # Get fixture data from disk
#     # ------------------------------------------------
#     example_data = helper.example_data_to_str("standard_default_config")
#     # ------------------------------------------------

#     base = tempfile.mkdtemp()
#     config_dir = tempfile.mkdtemp(prefix="config", dir=base)
#     config_file = os.path.join(config_dir, "config.yaml")

#     with open(config_file, "wt") as f:
#         f.write(example_data)

#     temp_config = yaml_load(config_file)

#     yield temp_config

#     shutil.rmtree(base)


# @pytest.fixture(scope="function")
# def fake_config_no_values():
#     """Create a temporary config file."""
#     base = tempfile.mkdtemp()
#     config_file = os.path.join(base, "config.yaml")

#     temp_config = yaml_load(config_file)

#     yield temp_config

#     shutil.rmtree(base)


# @pytest.fixture(scope="function")
# def fake_config_empty():
#     """Create a temporary config file."""
#     base = tempfile.mkdtemp()
#     config_file = os.path.join(base, "config.yaml")

#     with open(config_file, "wt") as f:
#         f.write(
#             """
# ---
# """
#         )
#     temp_config = yaml_load(config_file)

#     yield temp_config

#     shutil.rmtree(base)


# @pytest.mark.config
# @pytest.mark.unittest
# class TestConfigBase(object):
#     """Test the configutils."""

#     # Tests are not allowed to have an __init__ method
#     def setup_method(self, _):
#         """Set up called automatically before every test_XXXX method."""
#         self.log = logging.getLogger()
#         self.log.setLevel(logging.DEBUG)
#         logging.basicConfig(
#             format="%(filename)s:%(lineno)d (%(funcName)s): %(message)s"
#         )

#         self.cfg = None

#     def teardown_method(self, _):
#         """Tear down called automatically after every test_XXXX method."""
#         self.log.info("terminating Config")
#         self.cfg = None

#     def setup_config_instance(self):
#         assert self.cfg is None
#         self.log.info("Setting up config")
#         self.cfg = ultron8.config.Config()
#         self.log.info("Config instance created")

#     def setup_test(self):
#         """Setup Config Tests"""
#         self.setup_config_instance()


# @pytest.mark.config
# @pytest.mark.unittest
# class TestMoonbeamServiceConfigBase(object):
#     """Test the configutils."""

#     # Tests are not allowed to have an __init__ method
#     def setup_method(self, _):
#         """Set up called automatically before every test_XXXX method."""
#         self.log = logging.getLogger()
#         self.log.setLevel(logging.DEBUG)
#         logging.basicConfig(
#             format="%(filename)s:%(lineno)d (%(funcName)s): %(message)s"
#         )

#         self.m_cfg = None

#     def teardown_method(self, _):
#         """Tear down called automatically after every test_XXXX method."""
#         self.log.info("terminating Config")
#         self.m_cfg = None

#     def setup_config_instance(self):
#         assert self.m_cfg is None
#         self.log.info("Setting up config")
#         self.m_cfg = ultron8.config.MoonbeamServiceConfig()
#         self.log.info("MoonbeamServiceConfig instance created")

#     def setup_test(self):
#         """Setup Config Tests"""
#         self.setup_config_instance()


# class TestConfig(TestConfigBase):
#     """ Test config object
#     """

#     def test_config_default_instance(self):
#         """ Test basic Config instance
#         """
#         self.setup_test()

#         assert self.cfg.config_path == os.path.expanduser(
#             "~/.config/ultron8/config.yaml"
#         )
#         assert self.cfg.CONFIG_PATH == os.path.expanduser(
#             "~/.config/ultron8/config.yaml"
#         )
#         assert self.cfg.default_config == os.path.expanduser(
#             "{parent_dir}/ultron8/default_config.yaml".format(
#                 parent_dir=helper.get_parent_dir()
#             )
#         )
#         assert self.cfg.DEFAULT_CONFIG == os.path.expanduser(
#             "{parent_dir}/ultron8/default_config.yaml".format(
#                 parent_dir=helper.get_parent_dir()
#             )
#         )
#         assert self.cfg.profiles is None
#         assert self.cfg.profile_names == []

#     def test_config_modify_instance_properties(self):
#         """ Test modifying instance properties
#         """
#         self.setup_test()

#         # Defaults
#         assert self.cfg.config_path == os.path.expanduser(
#             "~/.config/ultron8/config.yaml"
#         )
#         assert self.cfg.default_config == os.path.expanduser(
#             "{parent_dir}/ultron8/default_config.yaml".format(
#                 parent_dir=helper.get_parent_dir()
#             )
#         )

#         self.cfg.config_path = "/made/up/path.yaml"
#         self.cfg.default_config = "/another/made/up/path.yaml"

#         # Make sure the private vars got updated
#         assert self.cfg._config_path == "/made/up/path.yaml"
#         assert self.cfg._default_config == "/another/made/up/path.yaml"


# @pytest.mark.config
# @pytest.mark.unittest
# class TestMoonbeamConfig(TestMoonbeamServiceConfigBase):
#     """ Test Moonbeam Config object
#     """

#     # SOURCE: https://github.com/ecorithm/eco_connect/blob/3b37856033d5e405abc7013ab40e0617d8e7b530/tests/unit/src/test_base_request.py
#     MODULE_PATH = 'ultron8.config'
#     CLASS_PATH = MODULE_PATH + '.MoonbeamServiceConfig'

#     def test_moonbeam_service_config_default_instance(self):
#         """ Test basic Moonbeam Service Config instance
#         """
#         self.setup_test()

#         assert (
#             self.m_cfg.git_repo
#             == "git@git.corp.adobe.com:behance/be-moonbeam-configs.git"
#         )
#         assert self.m_cfg.git_branch == "feature-code-build"
#         assert self.m_cfg.service_config_path == os.path.expanduser(
#             "~/.share/ultron8/be-moonbeam-configs"
#         )

#     def test_moonbeam_service_config_modify_instance_properties(self):
#         """ Test modifying instance properties
#         """
#         self.setup_test()

#         # Defaults
#         assert (
#             self.m_cfg.git_repo
#             == "git@git.corp.adobe.com:behance/be-moonbeam-configs.git"
#         )
#         assert self.m_cfg.git_branch == "feature-code-build"
#         assert self.m_cfg.service_config_path == os.path.expanduser(
#             "~/.share/ultron8/be-moonbeam-configs"
#         )

#         # Override
#         self.m_cfg.git_repo = "git@github.com:fake/fake-moonbeam-configs.git"
#         self.m_cfg.git_branch = "feature-fake"
#         self.m_cfg.service_config_path = "/fake/faker/fake-moonbeam-configs"

#         # test values
#         # Make sure the private vars got updated
#         assert self.m_cfg._git_repo == "git@github.com:fake/fake-moonbeam-configs.git"
#         assert self.m_cfg._git_branch == "feature-fake"
#         assert self.m_cfg._service_config_path == "/fake/faker/fake-moonbeam-configs"

#     # NOTE: This is currently broken till we finish mocking out the other tests
#     def test_moonbeam_service_config_load_fixture(self, fake_moonbeam_service_config, mocker):
#         """ Test modifying instance properties
#         """
#         self.setup_test()

#         share_dir, config_file, temp_config = fake_moonbeam_service_config

#         # Override
#         self.m_cfg.git_repo = "git@github.com:fake/fake-moonbeam-configs.git"
#         self.m_cfg.git_branch = "feature-fake"
#         self.m_cfg.service_config_path = share_dir

#         def mock_get_clone(git_repo, service_config_path, sha='master'):
#             pass

#         def mock_scm(service_config_path):
#             pass

#         def mock_remove(service_config_path):
#             pass

#         def mock_git_pull_rebase(git_repo, service_config_path, sha='master'):
#             pass

#         mocker.patch(self.MODULE_PATH + '.utils.git_clone', mock_get_clone)
#         mocker.patch(self.MODULE_PATH + '.utils.scm', mock_scm)
#         mocker.patch(self.MODULE_PATH + '.utils.remove', mock_remove)
#         mocker.patch(self.MODULE_PATH + '.utils.git_pull_rebase', mock_git_pull_rebase)


#         self.m_cfg.load_service("fake_moonbeam_app_code_deploy_service", "v2")
