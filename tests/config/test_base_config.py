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
import argparse

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


@pytest.mark.baseconfigonly
@pytest.mark.configonly
@pytest.mark.unittest
class TestBaseConfigSource:
    def test_configsource_invalid_filename(self):
        with pytest.raises(TypeError) as excinfo:
            config_base.ConfigSource({}, filename=1)
        assert "filename must be a string or None" in str(excinfo.value)

    def test_configsource_invalid_source_value(self):
        with pytest.raises(TypeError) as excinfo:
            config_base.ConfigSource.of("")
        assert "source value must be a dict" in str(excinfo.value)


@pytest.mark.baseconfigonly
@pytest.mark.configonly
@pytest.mark.unittest
class TestBaseConfigRootView:
    def test_rootview(self):

        sources = []
        cs1 = config_base.ConfigSource({1: 2}, filename="cs1.yaml")
        cs2 = config_base.ConfigSource({4: 5}, filename="cs2.yaml")

        sources.append(cs1)
        sources.append(cs2)

        temp_root = config_base.RootView(sources)

        assert temp_root.first() == (
            {1: 2},
            config_base.ConfigSource({1: 2}, "cs1.yaml", False),
        )

        # verify List/sequence emulation works and we can pull back keys 1 and 4
        contents = []
        for i in temp_root.all_contents():
            contents.append(i)

        assert 1 in contents
        assert 4 in contents

        # verify List/sequence emulation works for values()
        contents = []
        for i in temp_root.values():
            contents.append(str(i))

        assert "2" in contents
        assert "5" in contents

        # str view
        assert str(temp_root) == "{1: 2}"

        # verify contains func works as intented
        assert 1 in temp_root

        # verify set item works
        temp_root[9] = True
        contents = []
        for i in temp_root.all_contents():
            contents.append(i)

        assert 1 in contents
        assert 4 in contents
        assert 9 in contents

        # verify boolean view works
        assert bool(temp_root)
        # assert temp_root[1]

        # validate set_args function to pass in argeparse CLI values
        class C:
            pass

        c = C()
        parser = argparse.ArgumentParser()
        parser.add_argument("--foo")
        parser.parse_args(args=["--foo", "BAR"], namespace=c)

        temp_root.set_args(c)

        for k, v in temp_root.items():
            if str(k) == "foo":
                assert str(v) == "BAR"

        # Get root object
        assert str(type(temp_root.root())) == "<class 'ultron8.config.base.RootView'>"

        # set/get redactions
        temp_root.set_redaction(1, "***")

        str(temp_root.get_redactions()) == "{1}"

        # verify clear
        assert len(temp_root.sources) == 4
        temp_root.clear()
        assert len(temp_root.sources) == 0

    def test_subview(self):
        sources = []
        cs1 = config_base.ConfigSource({1: 2}, filename="cs1.yaml")
        cs2 = config_base.ConfigSource({4: 5}, filename="cs2.yaml")
        cs3 = config_base.ConfigSource({12: b"hi"}, filename="cs3.yaml")
        cs4 = config_base.ConfigSource({14: float(3.0)}, filename="cs4.yaml")

        sources.append(cs1)
        sources.append(cs2)
        sources.append(cs3)
        sources.append(cs4)

        temp_root = config_base.RootView(sources)

        contents = []
        for i in temp_root.values():
            contents.append(i)

        # contents
        # [<Subview: #1>, <Subview: #4>, <Subview: #12>, <Subview: #14>]

        # test that RootView is a parent for each of the Subviews
        for sv in contents:
            assert str(type(sv.root())) == "<class 'ultron8.config.base.RootView'>"

        # Test resolve func
        for v, s in contents[0].resolve():
            assert str(v) == "2"
            assert str(s) == "ConfigSource({1: 2}, 'cs1.yaml', False)"

    def test_rootview_first_not_found(self):
        sources = []

        temp_root = config_base.RootView(sources)

        # verify first value doesn't exist
        with pytest.raises(config_base.ConfigNotFoundError) as excinfo:
            temp_root.first()
        assert "root not found" in str(excinfo.value)

        # confirm class function exists returns False
        assert not temp_root.exists()

        # verify that we can not iterate
        with pytest.raises(TypeError) as excinfo:
            for i in temp_root:
                print(i)
        assert "'RootView' object is not iterable" in str(excinfo.value)

        # with pytest.raises(config_base.ConfigTypeError) as excinfo:
        #     for i in temp_root.all_contents():
        #         print(i)
        # assert "must be an iterable, not" in str(excinfo.value)
