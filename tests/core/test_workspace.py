import os
import shutil
import tempfile
import stat

from gettext import gettext as _

import pytest

from tests.conftest import fixtures_path
import ultron8
from ultron8.core import workspace

import logging

logger = logging.getLogger(__name__)


@pytest.mark.workspaceonly
@pytest.mark.unittest
class TestCliWorkspace(object):
    def test_directory_paths(self, mocker, monkeypatch):
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
            workspace, "config_dirs", return_value=expected_paths, autospec=True,
        )

        try:
            assert workspace.app_home() == "{}/ultron8".format(fake_dir)
            assert workspace.cluster_home() == "{}/ultron8/clusters".format(fake_dir)
            assert workspace.workspace_home() == "{}/ultron8/workspace".format(fake_dir)
            assert workspace.libs_home() == "{}/ultron8/libs".format(fake_dir)

        finally:
            # os.unlink(path)
            shutil.rmtree(base, ignore_errors=True)

    def test_mkdir_if_dne(self, mocker, monkeypatch):
        # create fake config directory
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        full_file_name = "directorythatdoesnotexist"
        path = os.path.join(fake_dir, full_file_name)

        mock_is_readable_dir = mocker.patch.object(
            workspace, "is_readable_dir", return_value={"result": False}, autospec=True,
        )

        mock_ensure_dir_exists = mocker.patch.object(
            workspace, "ensure_dir_exists", autospec=True,
        )

        # run test
        try:
            workspace.mkdir_if_dne(path)

            # tests
            mock_is_readable_dir.assert_called_once_with(path)
            mock_ensure_dir_exists.assert_called_once_with(path)

        finally:
            shutil.rmtree(base, ignore_errors=True)

    def test_prep_default_config(self, mocker, monkeypatch):
        # create fake config directory
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        full_file_name = "smart.yaml"
        path = os.path.join(fake_dir, "ultron8")
        full_path = os.path.join(path, full_file_name)

        mock_is_readable_dir = mocker.patch.object(
            workspace, "is_readable_dir", return_value={"result": False}, autospec=True,
        )
        mock_is_readable_file = mocker.patch.object(
            workspace,
            "is_readable_file",
            return_value={"result": False},
            autospec=True,
        )

        mock_ensure_dir_exists = mocker.patch.object(
            workspace, "ensure_dir_exists", autospec=True,
        )

        mock_config_manager = mocker.patch.object(
            workspace, "ConfigManager", autospec=True,
        )

        mock_app_home = mocker.patch.object(
            workspace,
            "app_home",
            return_value=os.path.join(fake_dir, "ultron8"),
            autospec=True,
        )

        # run test
        try:
            workspace.prep_default_config()

            # tests
            mock_config_manager.assert_called_once_with()
            mock_app_home.assert_called_once_with()
            mock_is_readable_file.assert_called_once_with(full_path)
            mock_ensure_dir_exists.assert_called_once_with(path)
            mock_is_readable_dir.assert_called_once_with(path)

        finally:
            shutil.rmtree(base, ignore_errors=True)

    # def test_app_home(self, mocker):
    #     pass
    #     path = "/opt/ultron8/fakefile.log"

    #     # run test
    #     result = paths.get_parent_dir(path)

    #     assert result == "/opt/ultron8"

    # def test_mkdir_p(self, mocker):
    #     # mock
    #     # mock_logger_info = mocker.MagicMock(name="mock_logger_info")
    #     mock_dir_exists = mocker.MagicMock(name="mock_dir_exists")
    #     mock_path = mocker.MagicMock(name="mock_path")
    #     # patch

    #     mocker.patch.object(ultron8.paths, "dir_exists", mock_dir_exists)
    #     mocker.patch.object(ultron8.paths, "Path", mock_path)

    #     path = "/opt/ultron8"

    #     mock_dir_exists.return_value = True

    #     # run test
    #     paths.mkdir_p(path)

    #     # assert
    #     mock_path.assert_called_once_with(path)

    #     mock_path().mkdir.assert_any_call(parents=True, exist_ok=True)

    # def test_dir_exists_false(self, mocker):
    #     # mock
    #     mock_path = mocker.MagicMock(name="mock_path")
    #     mocker.patch.object(ultron8.paths, "Path", mock_path)

    #     path = "/opt/ultron8"

    #     mock_path_instance = mock_path()

    #     mock_path_instance.is_dir.return_value = False

    #     # run test
    #     paths.dir_exists(path)

    #     assert mock_path_instance.is_dir.call_count == 2

    # def test_dir_exists_true(self, mocker):
    #     # mock

    #     mock_path = mocker.MagicMock(name="mock_path")

    #     mocker.patch.object(ultron8.paths, "Path", mock_path)

    #     path = "/opt/ultron8"

    #     mock_path_instance = mock_path()
    #     #
    #     mock_path_instance.is_dir.return_value = True

    #     # run test
    #     paths.dir_exists(path)

    #     # assert
    #     assert mock_path_instance.is_dir.call_count == 2

    # def test_mkdir_if_does_not_exist_false(self, mocker):
    #     # mock
    #     mock_mkdir_p = mocker.MagicMock(name="mock_mkdir_p")
    #     mock_dir_exists = mocker.MagicMock(name="mock_dir_exists", return_value=False)
    #     # patch
    #     mocker.patch.object(ultron8.paths, "mkdir_p", mock_mkdir_p)
    #     mocker.patch.object(ultron8.paths, "dir_exists", mock_dir_exists)

    #     path = "/opt/ultron8"

    #     # run test
    #     result = paths.mkdir_if_does_not_exist(path)

    #     # assert
    #     assert mock_mkdir_p.call_count == 1
    #     assert mock_dir_exists.call_count == 1
    #     assert result == True

    # def test_mkdir_if_does_not_exist_true(self, mocker):
    #     # mock
    #     mock_mkdir_p = mocker.MagicMock(name="mock_mkdir_p")
    #     mock_dir_exists = mocker.MagicMock(name="mock_dir_exists", return_value=True)
    #     # patch
    #     mocker.patch.object(ultron8.paths, "mkdir_p", mock_mkdir_p)
    #     mocker.patch.object(ultron8.paths, "dir_exists", mock_dir_exists)

    #     path = "/opt/ultron8"

    #     # run test
    #     result = paths.mkdir_if_does_not_exist(path)

    #     # assert
    #     assert mock_mkdir_p.call_count == 0
    #     assert mock_dir_exists.call_count == 1
    #     assert result == False

    # def test_fname_exists_true(self, mocker):
    #     # mock
    #     mock_path = mocker.MagicMock(name="mock_path")
    #     # patch
    #     mocker.patch.object(ultron8.paths, "Path", mock_path)

    #     path = "/opt/ultron8/generator.dot"

    #     mock_path_instance = mock_path()

    #     mock_path_instance.exists.return_value = True

    #     # run test
    #     result = paths.fname_exists(path)

    #     assert mock_path_instance.exists.call_count == 1
    #     mock_path.assert_any_call(path)
    #     assert result == True

    # def test_fname_exists_false(self, mocker):
    #     # mock
    #     mock_path = mocker.MagicMock(name="mock_path")
    #     # patch
    #     mocker.patch.object(ultron8.paths, "Path", mock_path)

    #     path = "/opt/ultron8/generator.dot"

    #     mock_path_instance = mock_path()

    #     mock_path_instance.exists.return_value = False

    #     # run test
    #     result = paths.fname_exists(path)

    #     assert mock_path_instance.exists.call_count == 1
    #     mock_path_instance.exists.assert_called_once_with()
    #     mock_path.assert_any_call(path)
    #     assert result == False

    # def test_dir_isWritable(self, mocker):
    #     # mock
    #     mock_os_access = mocker.MagicMock(name="mock_os_access")

    #     # patch
    #     mocker.patch.object(ultron8.paths.os, "access", mock_os_access)

    #     mock_is_readable_dir = mocker.patch.object(
    #         ultron8.paths,
    #         "is_readable_dir",
    #         return_value={"result": True},
    #         autospec=True,
    #     )

    #     path = "file:///tmp"

    #     mock_os_access.return_value = True

    #     # run test
    #     result = paths.isWritable(path)

    #     # tests
    #     mock_is_readable_dir.assert_called_once_with("file:///tmp")
    #     mock_os_access.assert_called_once_with("file:///tmp", os.W_OK)
    #     assert result == True

    # def test_file_isWritable(self, mocker):
    #     # mock
    #     mock_os_access = mocker.MagicMock(name="mock_os_access")
    #     # patch
    #     mocker.patch.object(ultron8.paths.os, "access", mock_os_access)
    #     # mock_is_readable_dir = mocker.patch.object(
    #     #     ultron8.paths, "is_readable_dir", return_value=False, autospec=True
    #     # )
    #     mock_is_readable_dir = mocker.patch.object(
    #         ultron8.paths,
    #         "is_readable_dir",
    #         return_value={"result": False},
    #         autospec=True,
    #     )

    #     path = "file:///tmp/fake_file"

    #     # patch return values
    #     mock_os_access.return_value = True

    #     # run test
    #     result = paths.isWritable(path)

    #     # tests
    #     mock_is_readable_dir.assert_called_once_with("file:///tmp/fake_file")
    #     mock_os_access.assert_called_once_with("file:///tmp", os.W_OK)
    #     assert result == True

    # def test_is_readable_dir_does_not_exist(self, mocker):
    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     full_file_name = "fake"
    #     path = os.path.join(fake_dir, full_file_name)

    #     res = paths.is_readable_dir(path)
    #     assert res["result"] == False
    #     assert res["message"] == "Path does not exist"

    # def test_is_readable_dir_does_exist_but_not_dir(self, mocker):
    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     full_file_name = "fake"
    #     path = os.path.join(fake_dir, full_file_name)

    #     logger.info(f"path: {path}")

    #     example_data = "fake data"

    #     try:
    #         with open(path, "wt") as f:
    #             f.write(example_data)

    #         res = paths.is_readable_dir(path)

    #     finally:
    #         os.unlink(path)

    #     assert res["result"] == False
    #     assert res["message"] == "Path is not a directory"

    # def test_is_readable_dir_exists_is_dir_but_not_readable(self, mocker):
    #     # SOURCE: https://docs.openstack.org/ironic/6.2.1/_modules/ironic/tests/unit/common/test_image_service.html
    #     mock_os_link = mocker.patch.object(ultron8.paths.os, "link", autospec=True)
    #     mock_os_remove = mocker.patch.object(ultron8.paths.os, "remove", autospec=True)
    #     mock_os_stat = mocker.patch.object(ultron8.paths.os, "stat", autospec=True)
    #     mock_os_isdir = mocker.patch.object(
    #         ultron8.paths.os.path, "isdir", autospec=True
    #     )
    #     mock_os_access = mocker.patch.object(
    #         ultron8.paths.os, "access", return_value=False, autospec=True
    #     )
    #     mock_exists = mocker.patch.object(
    #         ultron8.paths.os.path, "exists", return_value=True, autospec=True
    #     )

    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)

    #     path = fake_dir

    #     logger.info(f"path: {path}")

    #     try:

    #         res = paths.is_readable_dir(path)

    #     finally:
    #         os.rmdir(path)

    #     assert res["result"] == False
    #     assert res["message"] == "Directory is not readable"
    #     mock_os_access.assert_called_once_with(path, os.R_OK)

    # def test_is_readable_dir(self, mocker):
    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     path = fake_dir

    #     try:
    #         res = paths.is_readable_dir(path)
    #     finally:
    #         os.rmdir(path)
    #         # shutil.rmtree(tmpdir, ignore_errors=True)
    #     assert res["result"] == True

    # def test_is_readable_file_does_not_exist(self, mocker):
    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     full_file_name = "fake"
    #     path = os.path.join(fake_dir, full_file_name)

    #     res = paths.is_readable_file(path)
    #     assert res["result"] == False
    #     assert res["message"] == "Path does not exist"

    # def test_is_readable_file_does_exist_but_not_file(self, mocker):
    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     path = fake_dir

    #     logger.info(f"path: {path}")

    #     try:

    #         res = paths.is_readable_file(path)

    #     finally:
    #         os.rmdir(path)

    #     assert res["result"] == False
    #     assert res["message"] == "Path is not a file"

    # def test_is_readable_file_exists_is_file_but_not_readable(self, mocker):
    #     # SOURCE: https://docs.openstack.org/ironic/6.2.1/_modules/ironic/tests/unit/common/test_image_service.html
    #     mock_os_link = mocker.patch.object(ultron8.paths.os, "link", autospec=True)
    #     mock_os_remove = mocker.patch.object(ultron8.paths.os, "remove", autospec=True)
    #     mock_os_stat = mocker.patch.object(ultron8.paths.os, "stat", autospec=True)
    #     mock_os_isfile = mocker.patch.object(
    #         ultron8.paths.os.path, "isfile", autospec=True
    #     )
    #     mock_os_access = mocker.patch.object(
    #         ultron8.paths.os, "access", return_value=False, autospec=True
    #     )
    #     mock_exists = mocker.patch.object(
    #         ultron8.paths.os.path, "exists", return_value=True, autospec=True
    #     )

    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     full_file_name = "fake"
    #     path = os.path.join(fake_dir, full_file_name)

    #     logger.info(f"path: {path}")

    #     example_data = "test data"

    #     try:
    #         with open(path, "wt") as f:
    #             f.write(example_data)

    #         res = paths.is_readable_file(path)

    #     finally:
    #         os.unlink(path)
    #         # shutil.rmtree(tmpdir, ignore_errors=True)

    #     assert res["result"] == False
    #     assert res["message"] == "File is not readable"
    #     mock_os_access.assert_called_once_with(path, os.R_OK)

    # def test_is_readable_file(self, mocker):
    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     full_file_name = "fake"
    #     path = os.path.join(fake_dir, full_file_name)

    #     example_data = "test data"

    #     try:
    #         with open(path, "wt") as f:
    #             f.write(example_data)

    #         res = paths.is_readable_file(path)
    #     finally:
    #         os.unlink(path)
    #         # shutil.rmtree(tmpdir, ignore_errors=True)
    #     assert res["result"] == True

    # def test_ensure_dir_exists(self, mocker):
    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     directory = os.path.join(fake_dir, "fake", "as", "heck")

    #     logger.info(f"directory: {directory}")

    #     try:

    #         paths.ensure_dir_exists(directory)

    #         dir1 = os.path.join(fake_dir, "fake")
    #         dir2 = os.path.join(fake_dir, "fake", "as")
    #         dir3 = os.path.join(fake_dir, "fake", "as", "heck")

    #         assert oct(stat.S_IMODE(os.stat(dir1).st_mode)) == oct(493)  # same as 0o755
    #         assert oct(stat.S_IMODE(os.stat(dir2).st_mode)) == oct(493)
    #         assert oct(stat.S_IMODE(os.stat(dir3).st_mode)) == oct(493)

    #     finally:
    #         shutil.rmtree(fake_dir, ignore_errors=True)

    # def test_ensure_dir_exists_raise_exception(self, mocker):
    #     mock_os_makedirs = mocker.patch.object(
    #         ultron8.paths.os, "makedirs", side_effect=OSError, autospec=True
    #     )

    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     directory = os.path.join(fake_dir, "fake", "as", "heck")

    #     logger.info(f"directory: {directory}")

    #     with pytest.raises(Exception) as excinfo:
    #         paths.ensure_dir_exists(directory)

    #         assert "Cannot create directory " in str(excinfo.value)
    #         mock_os_makedirs.assert_called_once_with(directory, 0o775)

    # def test_ensure_file_exists(self, mocker):
    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     path = os.path.join(fake_dir, "test.log")

    #     logger.info(f"path: {path}")

    #     try:

    #         paths.ensure_file_exists(path, mode=0o600)

    #         assert oct(stat.S_IMODE(os.stat(path).st_mode)) == oct(384)  # same as 0o600

    #     finally:
    #         os.unlink(path)
    #         shutil.rmtree(base, ignore_errors=True)

    # def test_ensure_file_exists_raise_exception(self, mocker):
    #     mock_os_chmod = mocker.patch.object(
    #         ultron8.paths.os, "chmod", side_effect=IOError, autospec=True
    #     )

    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     path = os.path.join(fake_dir, "test.log")

    #     logger.info(f"path: {path}")

    #     with pytest.raises(Exception) as excinfo:
    #         paths.ensure_file_exists(path, mode=0o600)

    #         assert "Cannot create file " in str(excinfo.value)
    #         mock_os_chmod.assert_called_once_with(path, 0o600)

    # def test_get_permissions(self, mocker):
    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     path = os.path.join(fake_dir, "tester.log")

    #     logger.info(f"path: {path}")

    #     paths.ensure_file_exists(path, mode=0o600)

    #     assert paths.get_permissions(path) == oct(384)  # same as 0o600

    #     os.unlink(path)
    #     shutil.rmtree(base, ignore_errors=True)

    # def test_enforce_file_permissions(self, mocker):
    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     path = os.path.join(fake_dir, "tester.log")

    #     logger.info(f"path: {path}")

    #     paths.ensure_file_exists(path, mode=0o600)

    #     # change file permissions on purpose
    #     os.chmod(path, 0o644)

    #     with pytest.raises(Exception) as excinfo:
    #         paths.enforce_file_permissions(path)

    #         assert "File must only be accessible by owner. " in str(excinfo.value)

    #     os.unlink(path)
    #     shutil.rmtree(base, ignore_errors=True)

    # def test_enforce_file_permissions_file_does_not_exist(self, mocker):
    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     path = os.path.join(fake_dir, "tester.log")

    #     # Don't create actual file on purpose

    #     with pytest.raises(Exception) as excinfo:
    #         paths.enforce_file_permissions(path)

    #         assert f"Path [{path}] is not a file" in str(excinfo.value)

    #     shutil.rmtree(base, ignore_errors=True)

    # def test_path_to_uri(self):
    #     result = paths.path_to_uri("/etc/fstab")
    #     assert result == b"file:///etc/fstab"
    #     assert type(result) == bytes

    # def test_path_from_uri_bytes(self):
    #     raw_uri = b"file:///etc/fstab"
    #     result = paths.path_from_uri(raw_uri)
    #     assert result == "/etc/fstab"

    # def test_filename_from_uri_bytes(self):
    #     uri = b"file:///etc/fstab"
    #     result = paths.filename_from_uri(uri)
    #     assert result == "fstab"

    # def test_filename_from_uri_str(self):
    #     uri = "file:///etc/fstab"
    #     result = paths.filename_from_uri(uri)
    #     assert result == "fstab"

    # def test_quote_uri_byte_to_str(self):
    #     uri = b"file:///etc/fstab"
    #     result = paths.quote_uri(uri)
    #     assert result == "file:///etc/fstab"
    #     assert type(result) == str

    # def test_quantize(self):
    #     result = paths.quantize(100.00, 3.00)
    #     assert result == 99.0

    # def test_binary_search_EmptyList(self):
    #     assert paths.binary_search([], 10) == -1

    # def test_binary_search_Existing(self):
    #     A = [10, 20, 30]
    #     for index, element in enumerate(A):
    #         assert paths.binary_search([10, 20, 30], element) == index

    # def test_binary_search_MissingLeft(self):
    #     assert paths.binary_search([10, 20, 30], 1) == 0
    #     assert paths.binary_search([10, 20, 30], 16) == 1
    #     assert paths.binary_search([10, 20, 30], 29) == 2

    # def test_binary_search_MissingRight(self):
    #     assert paths.binary_search([10, 20, 30], 11) == 0
    #     assert paths.binary_search([10, 20, 30], 24) == 1
    #     assert paths.binary_search([10, 20, 30], 40) == 2

    # def test_uri_to_path_str(self):
    #     uri = "file:///etc/fstab"
    #     result = paths.uri_to_path(uri)
    #     assert result == "/etc/fstab"

    # def test_uri_to_path_bytes(self):
    #     uri = b"file:///etc/fstab"
    #     result = paths.uri_to_path(uri)
    #     assert result == "/etc/fstab"

    # def test_is_pathname_valid(self, mocker):
    #     assert paths.is_pathname_valid("foo.bar")
    #     # Long path valid?
    #     assert not paths.is_pathname_valid("a" * 256)
    #     assert not paths.is_pathname_valid(None)

    # def test_is_path_creatable(self, mocker):
    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     full_file_name = "fake"
    #     path = os.path.join(fake_dir, full_file_name)

    #     assert paths.is_path_creatable(path)
    #     assert not paths.is_path_creatable("/bossjones/is/the/best/file.txt")

    #     shutil.rmtree(base, ignore_errors=True)

    # def test_is_path_exists_or_creatable(self, mocker):
    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     full_file_name = "fake"
    #     path = os.path.join(fake_dir, full_file_name)

    #     assert paths.is_path_exists_or_creatable(path)

    #     assert not paths.is_path_exists_or_creatable("/bossjones/is/the/best/file.txt")

    #     shutil.rmtree(base, ignore_errors=True)

    # def test_is_path_sibling_creatable(self, mocker):
    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     full_file_name = "fake"
    #     path = os.path.join(fake_dir, full_file_name)

    #     assert paths.is_path_sibling_creatable(path)

    #     assert not paths.is_path_sibling_creatable("/bossjones/is/the/best/file.txt")

    #     shutil.rmtree(base, ignore_errors=True)

    # def test_is_path_exists_or_creatable_portable(self, mocker):
    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     full_file_name = "fake"
    #     path = os.path.join(fake_dir, full_file_name)

    #     assert paths.is_path_exists_or_creatable_portable(path)

    #     assert not paths.is_path_exists_or_creatable_portable(
    #         "/bossjones/is/the/best/file.txt"
    #     )

    #     shutil.rmtree(base, ignore_errors=True)
