"""Test Global Config."""
# pylint: disable=protected-access
import logging
import os
import tempfile
import shutil
import pytest
import pyconfig

import ultron8
from ultron8.config import do_set_flag
from ultron8.config import do_get_flag
from ultron8.config import do_set_multi_flag

# from ultron8.config import ULTRON_CLI_BASE_CONFIG_DIRECTORY
# from ultron8.config import ULTRON_CONFIG_DIRECTORY
# from ultron8.config import ULTRON_CONFIG_PATH
# from ultron8.config import ULTRON_CLUSTERS_PATH
# from ultron8.config import ULTRON_CACHE_PATH
# from ultron8.config import ULTRON_WORKSPACE_PATH
# from ultron8.config import ULTRON_LIBS_PATH
# from ultron8.config import ULTRON_TEMPLATES_PATH

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def fake_dir() -> str:
    base_dir = tempfile.mkdtemp()
    logger.info(f"BASE_DIR: {base_dir}")

    yield base_dir

    # shutil.rmtree(base_dir)


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
