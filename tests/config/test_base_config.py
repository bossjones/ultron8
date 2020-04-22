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
def user_config_fixture() -> str:
    user_config_fixture = """
---
clusters_path: clusters/
cache_path: cache/
workspace_path: workspace/
templates_path: templates/

# beard_paths:
#   - beards/
#   - beard_cache/

ultrons:
  - debugultron

async: True

nodes: 0

# stache_paths:
#   - moustaches

# staches:
#   - postcats

db_uri: sqlite:///test.db
# db_bin_path: ./db_binary_entries

# admins:
#   [
#   [My name, 99999999],
#   ]

# host: 0.0.0.0
# port: 8000

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
            token: ''
"""
    yield user_config_fixture


@pytest.fixture(scope="function")
def all_types_fixture() -> str:
    all_types_fixture = """
---
utf8: "Это уникодная строка"

test_list_of_strings:
  - Boston Red Sox
  - Detroit Tigers
  - New York Yankees

test_bools:
- yes
- NO
- True
- on

test_map_of_floats:
  canonical: 6.8523015e+5
  exponential: 685.230_15e+03
  fixed: 685_230.15
  sexagesimal: 190:20:30.15
  negative infinity: -.inf
  not a number: .NaN

42: life the universe everything

test_list_of_ints:
    - 21
    - 1
    - 2
    - 3
    - 1911

test_small_list:
    - 1
    - 2
"""
    yield all_types_fixture


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


@pytest.mark.baseconfigonly
@pytest.mark.configonly
@pytest.mark.unittest
class TestBaseConfigDirs:
    def test_config_dirs_domain_user(self):
        actual_paths = config_base.config_dirs(domain="user", override=None)
        default_path = os.path.abspath(os.path.expanduser("~/.config"))
        expected_paths = []
        expected_paths.append(default_path)

        assert actual_paths == expected_paths  # ~/.config

    def test_config_dirs_domain_system(self):
        actual_paths = config_base.config_dirs(domain="system", override=None)
        default_path = os.path.abspath(os.path.expanduser("/etc/ultron8"))
        expected_paths = []
        expected_paths.append(default_path)

        assert actual_paths == expected_paths  # /etc/ultron8

    def test_config_dirs_domain_system_override(self):
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)

        actual_paths = config_base.config_dirs(domain="system", override=fake_dir)
        default_path = os.path.abspath(os.path.expanduser(fake_dir))
        expected_paths = []
        expected_paths.append(default_path)

        assert actual_paths == expected_paths  # /tmp/blahblahconfig

        shutil.rmtree(base, ignore_errors=True)


@pytest.mark.baseconfigonly
@pytest.mark.configonly
@pytest.mark.unittest
class TestBaseConfigBaseConfigurationView:
    def test_base_configuration_view(self, user_config_fixture, mocker):
        # create fake config directory
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        full_file_name = "smart.yaml"
        path = os.path.join(fake_dir, full_file_name)

        # create fake fixture data to be returned as list(<fake_dir>)
        default_path = os.path.abspath(os.path.expanduser(fake_dir))
        expected_paths = []
        expected_paths.append(default_path)

        mock_config_dirs = mocker.patch.object(
            config_base, "config_dirs", return_value=expected_paths, autospec=True,
        )

        # write temporary data to disk
        example_data = user_config_fixture
        try:
            with open(path, "wt") as f:
                f.write(example_data)

            # create base config and test it out
            bcv = config_base.BaseConfiguration("ultron8", "ultron8.config", read=True)

            assert bcv.appname == "ultron8"
            assert bcv.config_filename == "smart.yaml"
            assert bcv.default_filename == "smart_default.yaml"
            assert bcv.domain == "user"
            assert bcv.modname == "ultron8.config"
            assert bcv.name == "root"
            assert bcv._env_var == "ULTRON8DIR"

            mock_config_dirs.assert_called_once_with(domain="user")

            assert (
                bcv.dump()
                == "clusters_path: clusters/\ncache_path: cache/\nworkspace_path: workspace/\ntemplates_path: templates/\n\n# beard_paths:\n#   - beards/\n#   - beard_cache/\n\n# beards:\n#   - debugbeard\n\n# stache_paths:\n#   - moustaches\n\n# staches:\n#   - postcats\n\n# db_url: sqlite:///skybeard-2.db\n# db_bin_path: ./db_binary_entries\n\n# admins:\n#   [\n#   [My name, 99999999],\n#   ]\n\n# host: 0.0.0.0\n# port: 8000\n\nflags:\n    debug: 0\n    verbose: 0\n    keep: 0\n    stderr: 0\n    repeat: 1\n\nclusters:\n    instances:\n        local:\n            url: http://localhost:11267\n            token: ''\n"
            )

            # FIXME: This empty dict, is that what we actually want when we say don't use full dump?
            assert bcv.dump(full=False) == "{}\n"
            print(bcv)

        finally:
            os.unlink(path)
            shutil.rmtree(base, ignore_errors=True)

    def test_base_configuration_view_envvar_invalid_file(
        self, user_config_fixture, mocker, monkeypatch
    ):
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
        monkeypatch.setenv("ULTRON8DIR", path)
        mock_config_dirs = mocker.patch.object(
            config_base, "config_dirs", return_value=expected_paths, autospec=True,
        )

        # write temporary data to disk
        example_data = user_config_fixture

        with open(path, "wt") as f:
            f.write(example_data)

        with pytest.raises(config_base.ConfigError) as excinfo:
            bcv = config_base.BaseConfiguration("ultron8", "ultron8.config", read=True)
        assert "ULTRON8DIR must be a directory" in str(excinfo.value)
        assert mock_config_dirs.call_count == 0

        print(path)
        print(base)

        os.unlink(path)
        shutil.rmtree(base, ignore_errors=True)

    def test_base_configuration_view_envvar(
        self, user_config_fixture, mocker, monkeypatch
    ):
        # create fake config directory
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        full_file_name = "smart.yaml"
        full_file_name2 = "smart2.yaml"
        path = os.path.join(fake_dir, full_file_name)
        path2 = os.path.join(fake_dir, full_file_name2)

        override_data = """
clusters:
    instances:
        local:
            url: 'http://localhost:11267'
            token: 'blahblahblahblahfake'
"""

        # create fake fixture data to be returned as list(<fake_dir>)
        default_path = os.path.abspath(os.path.expanduser(fake_dir))
        expected_paths = []
        expected_paths.append(default_path)

        # temporarily patch environment to include fake_dir
        monkeypatch.setenv("ULTRON8DIR", fake_dir)
        mocker.patch.object(
            config_base, "config_dirs", return_value=expected_paths, autospec=True,
        )

        # write temporary data to disk
        example_data = user_config_fixture

        try:
            with open(path, "wt") as f:
                f.write(example_data)

            with open(path2, "wt") as f:
                f.write(override_data)

            bcv = config_base.BaseConfiguration("ultron8", "ultron8.config", read=True)

            # Since we configured it to read off the bat, we should expect 2 config sources be present. 1. from the env var, and the 2nd from the default config
            assert len(bcv.sources) == 2

            # Parses the file as YAML and inserts it into the configuration sources with highest priority.
            bcv.set_file(path2)
            bcv.read(source=False, defaults=False)

            # Since we configured it to read off the bat, we should expect 3 config sources be present. 1. from the env var, and the 2nd from the default config, 3rd from path2
            assert len(bcv.sources) == 3

            print(path)
            print(base)

        finally:

            os.unlink(path)
            os.unlink(path2)
            shutil.rmtree(base, ignore_errors=True)


@pytest.mark.baseconfigonly
@pytest.mark.configonly
@pytest.mark.unittest
class TestBaseConfigTemplates:
    def test_template_with_sentinel(self, all_types_fixture, mocker, monkeypatch):

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
        mocker.patch.object(
            config_base, "config_dirs", return_value=expected_paths, autospec=True,
        )

        mock_as_template = mocker.patch.object(
            config_base, "as_template", autospec=True,
        )

        # write temporary data to disk
        example_data = all_types_fixture

        try:
            with open(path, "wt") as f:
                f.write(example_data)

            bcv = config_base.BaseConfiguration("ultron8", "ultron8.config", read=False)

            bcv.read(source=True, defaults=False)

            print(path)
            print(base)

            s = bcv.sources[0]

            assert s.get("test_bools") == [True, False, True, True]
            assert s.get("test_list_of_ints") == [21, 1, 2, 3, 1911]
            assert s.get("test_list_of_strings") == [
                "Boston Red Sox",
                "Detroit Tigers",
                "New York Yankees",
            ]
            # assert s.get("test_map_of_floats")["canonical") == 6.8523015e+5
            assert s.get("utf8") == "Это уникодная строка"
            assert s.get(42) == "life the universe everything"
            # assert s.default == False

        finally:
            os.unlink(path)
            shutil.rmtree(base, ignore_errors=True)
