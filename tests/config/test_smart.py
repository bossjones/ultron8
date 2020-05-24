"""Test Smart Config."""
# pylint: disable=protected-access
import logging
import os
import shutil
import tempfile

import pyconfig
import pytest

import ultron8

# from ultron8.config import smart

# logger = logging.getLogger(__name__)

# # def create_file(path):
# #     """Create an empty file."""
# #     with open(path, "w"):
# #         pass


# # @pytest.fixture(scope="function")
# # def fake_dir() -> str:
# #     base_dir = tempfile.mkdtemp()
# #     logger.info(f"BASE_DIR: {base_dir}")

# #     yield base_dir

# #     # shutil.rmtree(base_dir)


# # @pytest.fixture(scope="function")
# # def spoof_config_dir_base_path() -> str:
# #     base = tempfile.mkdtemp()
# #     base_dir = tempfile.mkdtemp(prefix="config", dir=base)

# #     yield base_dir

# #     shutil.rmtree(base_dir, ignore_errors=True)


# @pytest.fixture
# def cf():
#     return smart.get_config()


# @pytest.mark.smartonly
# @pytest.mark.configonly
# @pytest.mark.unittest
# class TestSmartConfig:
#     def test_is_singleton(self, cf):
#         newcf = smart.get_config()
#         assert id(newcf) == id(cf)

#     def test_read_default(self, cf):
#         assert cf["flags"]["debug"] == 0
#         assert cf["flags"]["verbose"] == 0

#     def test_attribute_access(self, cf):
#         cf.flags.debug = 1
#         assert cf.flags.debug == 1


# class TestSmartConfigUpdate:
#     def test_with_initdict(self):
#         smart._CONFIG = None
#         cf = smart.get_config(initdict={"base.tree": "value"})
#         assert cf.base.tree == "value"


# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
