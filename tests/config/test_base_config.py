"""Test Base Config."""
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
from ultron8.config import base as config_base


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


@pytest.mark.baseconfigonly
@pytest.mark.configonly
@pytest.mark.unittest
class TestBaseConfig:
    def test_load_yaml_error_tabs(self):
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        full_file_name = "fake.yaml"
        path = os.path.join(fake_dir, full_file_name)

        example_data = """
\t\t:
  hello: 'world'
"""
        try:
            with open(path, "wt") as f:
                f.write(example_data)

            with pytest.raises(config_base.ConfigReadError) as excinfo:
                config_base.load_yaml(path)
            assert "file {0} could not be read: found tab character at line 2, column 1".format(
                path
            ) in str(
                excinfo.value
            )

        finally:
            os.unlink(path)
            shutil.rmtree(base, ignore_errors=True)

    def test_load_yaml_error_invalid_file(self):
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        full_file_name = "fake.yaml"
        path = os.path.join(fake_dir, full_file_name)

        example_data = """
me: me: me: me:
"""
        try:
            with open(path, "wt") as f:
                f.write(example_data)

            with pytest.raises(config_base.ConfigReadError) as excinfo:
                config_base.load_yaml(path)
            assert "file {0} could not be read: mapping values are not allowed here".format(
                path
            ) in str(
                excinfo.value
            )

        finally:
            os.unlink(path)
            shutil.rmtree(base, ignore_errors=True)
