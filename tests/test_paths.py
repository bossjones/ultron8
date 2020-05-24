# import shutil
# from contextlib import contextmanager
# from uuid import uuid4

# import pyconfig

import os
import shutil
import tempfile
import stat

# import unittest

from gettext import gettext as _

import pytest

from tests.conftest import fixtures_path
import ultron8
from ultron8 import paths

import logging
from pytest_mock.plugin import MockFixture

logger = logging.getLogger(__name__)

# from typing import Iterator

# @pytest.mark.parametrize(
#     "test_input,expected",
#     [
#         (
#             "http://stackoverflow.com:8080/some/folder?test=/questions/9626535/get-domain-name-from-url",
#             "stackoverflow.com",
#         ),
#         (
#             "Stackoverflow.com:8080/some/folder?test=/questions/9626535/get-domain-name-from-url",
#             "stackoverflow.com",
#         ),
#         (
#             "http://stackoverflow.com/some/folder?test=/questions/9626535/get-domain-name-from-url",
#             "stackoverflow.com",
#         ),
#         (
#             "https://StackOverflow.com:8080?test=/questions/9626535/get-domain-name-from-url",
#             "stackoverflow.com",
#         ),
#         (
#             "stackoverflow.com?test=questions&v=get-domain-name-from-url",
#             "stackoverflow.com",
#         ),
#     ],
# )
# def test_get_domain_from_fqdn(test_input, expected):
#     assert str(get_domain_from_fqdn(test_input)) == expected


def bad_read():
    raise UnicodeDecodeError("utf-8", b"0x80", 0, 1, "invalid start byte")


@pytest.mark.pathsonly
@pytest.mark.unittest
class TestPathToFileURI(object):
    def test_get_parent_dir(self, mocker: MockFixture) -> None:
        path = "/opt/ultron8/fakefile.log"

        # run test
        result = paths.get_parent_dir(path)

        assert result == "/opt/ultron8"

    def test_mkdir_p(self, mocker: MockFixture) -> None:
        # mock
        # mock_logger_info = mocker.MagicMock(name="mock_logger_info")
        mock_dir_exists = mocker.MagicMock(name="mock_dir_exists")
        mock_path = mocker.MagicMock(name="mock_path")
        # patch

        mocker.patch.object(ultron8.paths, "dir_exists", mock_dir_exists)
        mocker.patch.object(ultron8.paths, "Path", mock_path)

        path = "/opt/ultron8"

        mock_dir_exists.return_value = True

        # run test
        paths.mkdir_p(path)

        # assert
        mock_path.assert_called_once_with(path)

        mock_path().mkdir.assert_any_call(parents=True, exist_ok=True)

    def test_dir_exists_false(self, mocker: MockFixture) -> None:
        # mock
        # mock_logger_error = mocker.MagicMock(name="mock_logger_error")
        mock_path = mocker.MagicMock(name="mock_path")
        # patch
        # mocker.patch.object(
        #     scarlett_os.subprocess.logging.Logger, "error", mock_logger_error
        # )
        mocker.patch.object(ultron8.paths, "Path", mock_path)

        path = "/opt/ultron8"

        mock_path_instance = mock_path()

        mock_path_instance.is_dir.return_value = False

        # run test
        paths.dir_exists(path)

        # assert
        # assert mock_logger_error.call_count == 1
        assert mock_path_instance.is_dir.call_count == 2
        # mock_logger_error.assert_any_call("This is not a dir: {}".format(path))

    def test_dir_exists_true(self, mocker: MockFixture) -> None:
        # mock
        # mock_logger_error = mocker.MagicMock(name="mock_logger_error")
        mock_path = mocker.MagicMock(name="mock_path")
        # patch
        # mocker.patch.object(
        #     scarlett_os.subprocess.logging.Logger, "error", mock_logger_error
        # )
        mocker.patch.object(ultron8.paths, "Path", mock_path)

        path = "/opt/ultron8"

        mock_path_instance = mock_path()
        #
        mock_path_instance.is_dir.return_value = True

        # run test
        paths.dir_exists(path)

        # assert
        # assert mock_logger_error.call_count == 0
        assert mock_path_instance.is_dir.call_count == 2
        # mock_logger_error.assert_not_called()

    def test_mkdir_if_does_not_exist_false(self, mocker: MockFixture) -> None:
        # mock
        mock_mkdir_p = mocker.MagicMock(name="mock_mkdir_p")
        mock_dir_exists = mocker.MagicMock(name="mock_dir_exists", return_value=False)
        # patch
        mocker.patch.object(ultron8.paths, "mkdir_p", mock_mkdir_p)
        mocker.patch.object(ultron8.paths, "dir_exists", mock_dir_exists)

        path = "/opt/ultron8"

        # run test
        result = paths.mkdir_if_does_not_exist(path)

        # assert
        assert mock_mkdir_p.call_count == 1
        assert mock_dir_exists.call_count == 1
        assert result == True

    def test_mkdir_if_does_not_exist_true(self, mocker: MockFixture) -> None:
        # mock
        mock_mkdir_p = mocker.MagicMock(name="mock_mkdir_p")
        mock_dir_exists = mocker.MagicMock(name="mock_dir_exists", return_value=True)
        # patch
        mocker.patch.object(ultron8.paths, "mkdir_p", mock_mkdir_p)
        mocker.patch.object(ultron8.paths, "dir_exists", mock_dir_exists)

        path = "/opt/ultron8"

        # run test
        result = paths.mkdir_if_does_not_exist(path)

        # assert
        assert mock_mkdir_p.call_count == 0
        assert mock_dir_exists.call_count == 1
        assert result == False

    def test_fname_exists_true(self, mocker: MockFixture) -> None:
        # mock
        mock_path = mocker.MagicMock(name="mock_path")
        # patch
        mocker.patch.object(ultron8.paths, "Path", mock_path)

        path = "/opt/ultron8/generator.dot"

        mock_path_instance = mock_path()

        mock_path_instance.exists.return_value = True

        # run test
        result = paths.fname_exists(path)

        assert mock_path_instance.exists.call_count == 1
        mock_path.assert_any_call(path)
        assert result == True

    # def test_touch_empty_file(self, mocker):
    #     # mock
    #     # mock_os_link = mocker.patch.object(ultron8.paths, "fname_exists", autospec=True)

    #     # mock_path = mocker.MagicMock(name="mock_path")
    #     # patch
    #     # mocker.patch.object(ultron8.paths, "Path", mock_path)

    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     full_file_name = "fake"
    #     path = os.path.join(fake_dir, full_file_name)

    #     try:
    #         # run test
    #         res = paths.touch_empty_file(path)

    #         assert paths.fname_exists(path)
    #         assert res
    #     finally:
    #         os.unlink(path)
    #         shutil.rmtree(base, ignore_errors=True)

    # # TODO:
    # def test_touch_empty_file_when_it_already_exists(self, mocker):
    #     mock_fname_exists = mocker.patch.object(
    #         ultron8.paths, "fname_exists", return_value=False,autospec=True
    #     )

    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     full_file_name = "fake"
    #     path = os.path.join(fake_dir, full_file_name)

    #     example_data = "fake data"

    #     with open(path, "wt") as f:
    #         f.write(example_data)

    #     with pytest.raises(Exception) as excinfo:
    #         paths.touch_empty_file(path)

    #         assert mock_fname_exists.assert_called_once_with(path)

    #         assert f"Cannot create touch file [{path}]: " in str(excinfo.value)

    #     os.unlink(path)
    #     shutil.rmtree(base, ignore_errors=True)

    def test_fname_exists_false(self, mocker: MockFixture) -> None:
        # mock
        mock_path = mocker.MagicMock(name="mock_path")
        # patch
        mocker.patch.object(ultron8.paths, "Path", mock_path)

        path = "/opt/ultron8/generator.dot"

        mock_path_instance = mock_path()

        mock_path_instance.exists.return_value = False

        # run test
        result = paths.fname_exists(path)

        assert mock_path_instance.exists.call_count == 1
        mock_path_instance.exists.assert_called_once_with()
        mock_path.assert_any_call(path)
        assert result == False

    def test_dir_isWritable(self, mocker: MockFixture) -> None:
        # mock
        mock_os_access = mocker.MagicMock(name="mock_os_access")

        # patch
        mocker.patch.object(ultron8.paths.os, "access", mock_os_access)

        mock_is_readable_dir = mocker.patch.object(
            ultron8.paths,
            "is_readable_dir",
            return_value={"result": True},
            autospec=True,
        )

        path = "file:///tmp"

        mock_os_access.return_value = True

        # run test
        result = paths.isWritable(path)

        # tests
        mock_is_readable_dir.assert_called_once_with("file:///tmp")
        mock_os_access.assert_called_once_with("file:///tmp", os.W_OK)
        assert result == True

    def test_file_isWritable(self, mocker: MockFixture) -> None:
        # mock
        mock_os_access = mocker.MagicMock(name="mock_os_access")
        # patch
        mocker.patch.object(ultron8.paths.os, "access", mock_os_access)
        # mock_is_readable_dir = mocker.patch.object(
        #     ultron8.paths, "is_readable_dir", return_value=False, autospec=True
        # )
        mock_is_readable_dir = mocker.patch.object(
            ultron8.paths,
            "is_readable_dir",
            return_value={"result": False},
            autospec=True,
        )

        path = "file:///tmp/fake_file"

        # patch return values
        mock_os_access.return_value = True

        # run test
        result = paths.isWritable(path)

        # tests
        mock_is_readable_dir.assert_called_once_with("file:///tmp/fake_file")
        mock_os_access.assert_called_once_with("file:///tmp", os.W_OK)
        assert result == True

    def test_is_readable_dir_does_not_exist(self, mocker: MockFixture) -> None:
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        full_file_name = "fake"
        path = os.path.join(fake_dir, full_file_name)

        res = paths.is_readable_dir(path)
        assert res["result"] == False
        assert res["message"] == "Path does not exist"

    def test_is_readable_dir_does_exist_but_not_dir(self, mocker: MockFixture) -> None:
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        full_file_name = "fake"
        path = os.path.join(fake_dir, full_file_name)

        logger.info(f"path: {path}")

        example_data = "fake data"

        try:
            with open(path, "wt") as f:
                f.write(example_data)

            res = paths.is_readable_dir(path)

        finally:
            os.unlink(path)

        assert res["result"] == False
        assert res["message"] == "Path is not a directory"

    def test_is_readable_dir_exists_is_dir_but_not_readable(
        self, mocker: MockFixture
    ) -> None:
        # SOURCE: https://docs.openstack.org/ironic/6.2.1/_modules/ironic/tests/unit/common/test_image_service.html
        mock_os_link = mocker.patch.object(ultron8.paths.os, "link", autospec=True)
        mock_os_remove = mocker.patch.object(ultron8.paths.os, "remove", autospec=True)
        mock_os_stat = mocker.patch.object(ultron8.paths.os, "stat", autospec=True)
        mock_os_isdir = mocker.patch.object(
            ultron8.paths.os.path, "isdir", autospec=True
        )
        mock_os_access = mocker.patch.object(
            ultron8.paths.os, "access", return_value=False, autospec=True
        )
        mock_exists = mocker.patch.object(
            ultron8.paths.os.path, "exists", return_value=True, autospec=True
        )

        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)

        path = fake_dir

        logger.info(f"path: {path}")

        try:

            res = paths.is_readable_dir(path)

        finally:
            os.rmdir(path)
            # shutil.rmtree(tmpdir, ignore_errors=True)

        assert res["result"] == False
        assert res["message"] == "Directory is not readable"
        mock_os_access.assert_called_once_with(path, os.R_OK)

    def test_is_readable_dir(self, mocker: MockFixture) -> None:
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        path = fake_dir

        try:
            res = paths.is_readable_dir(path)
        finally:
            os.rmdir(path)
            # shutil.rmtree(tmpdir, ignore_errors=True)
        assert res["result"] == True

        # def test_file_isReadable(self):
        #     fd_unused, path = tempfile.mkstemp(suffix=".wav")

        #     try:
        #         # run test
        #         result = paths.isReadable(path)

        #         # tests
        #         assert result
        #     finally:
        #         os.remove(path)

    def test_is_readable_file_does_not_exist(self, mocker: MockFixture) -> None:
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        full_file_name = "fake"
        path = os.path.join(fake_dir, full_file_name)

        res = paths.is_readable_file(path)
        assert res["result"] == False
        assert res["message"] == "Path does not exist"

    def test_is_readable_file_does_exist_but_not_file(
        self, mocker: MockFixture
    ) -> None:
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        path = fake_dir

        logger.info(f"path: {path}")

        try:

            res = paths.is_readable_file(path)

        finally:
            os.rmdir(path)

        assert res["result"] == False
        assert res["message"] == "Path is not a file"

    def test_is_readable_file_exists_is_file_but_not_readable(
        self, mocker: MockFixture
    ) -> None:
        # SOURCE: https://docs.openstack.org/ironic/6.2.1/_modules/ironic/tests/unit/common/test_image_service.html
        mock_os_link = mocker.patch.object(ultron8.paths.os, "link", autospec=True)
        mock_os_remove = mocker.patch.object(ultron8.paths.os, "remove", autospec=True)
        mock_os_stat = mocker.patch.object(ultron8.paths.os, "stat", autospec=True)
        mock_os_isfile = mocker.patch.object(
            ultron8.paths.os.path, "isfile", autospec=True
        )
        mock_os_access = mocker.patch.object(
            ultron8.paths.os, "access", return_value=False, autospec=True
        )
        mock_exists = mocker.patch.object(
            ultron8.paths.os.path, "exists", return_value=True, autospec=True
        )

        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        full_file_name = "fake"
        path = os.path.join(fake_dir, full_file_name)

        logger.info(f"path: {path}")

        example_data = "test data"

        try:
            with open(path, "wt") as f:
                f.write(example_data)

            res = paths.is_readable_file(path)

        finally:
            os.unlink(path)
            # shutil.rmtree(tmpdir, ignore_errors=True)

        assert res["result"] == False
        assert res["message"] == "File is not readable"
        mock_os_access.assert_called_once_with(path, os.R_OK)

    def test_is_readable_file(self, mocker: MockFixture) -> None:
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        full_file_name = "fake"
        path = os.path.join(fake_dir, full_file_name)

        example_data = "test data"

        try:
            with open(path, "wt") as f:
                f.write(example_data)

            res = paths.is_readable_file(path)
        finally:
            os.unlink(path)
            # shutil.rmtree(tmpdir, ignore_errors=True)
        assert res["result"] == True

    def test_ensure_dir_exists(self, mocker: MockFixture) -> None:
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        directory = os.path.join(fake_dir, "fake", "as", "heck")

        logger.info(f"directory: {directory}")

        try:

            paths.ensure_dir_exists(directory)

            dir1 = os.path.join(fake_dir, "fake")
            dir2 = os.path.join(fake_dir, "fake", "as")
            dir3 = os.path.join(fake_dir, "fake", "as", "heck")

            print(f"dir1: {dir1}")
            print(f"dir1: {dir2}")
            print(f"dir1: {dir3}")
            assert oct(stat.S_IMODE(os.stat(dir1).st_mode)) == oct(493)  # same as 0o755
            assert oct(stat.S_IMODE(os.stat(dir2).st_mode)) == oct(493)
            assert oct(stat.S_IMODE(os.stat(dir3).st_mode)) == oct(493)

        finally:
            shutil.rmtree(fake_dir, ignore_errors=True)

    def test_ensure_dir_exists_raise_exception(self, mocker: MockFixture) -> None:
        mock_os_makedirs = mocker.patch.object(
            ultron8.paths.os, "makedirs", side_effect=OSError, autospec=True
        )

        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        directory = os.path.join(fake_dir, "fake", "as", "heck")

        logger.info(f"directory: {directory}")

        with pytest.raises(Exception) as excinfo:
            paths.ensure_dir_exists(directory)

            assert "Cannot create directory " in str(excinfo.value)
            mock_os_makedirs.assert_called_once_with(directory, 0o775)

    def test_ensure_file_exists(self, mocker: MockFixture) -> None:
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        path = os.path.join(fake_dir, "test.log")

        logger.info(f"path: {path}")

        try:

            paths.ensure_file_exists(path, mode=0o600)

            assert oct(stat.S_IMODE(os.stat(path).st_mode)) == oct(384)  # same as 0o600

        finally:
            os.unlink(path)
            shutil.rmtree(base, ignore_errors=True)

    def test_ensure_file_exists_raise_exception(self, mocker: MockFixture) -> None:
        mock_os_chmod = mocker.patch.object(
            ultron8.paths.os, "chmod", side_effect=IOError, autospec=True
        )

        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        path = os.path.join(fake_dir, "test.log")

        logger.info(f"path: {path}")

        with pytest.raises(Exception) as excinfo:
            paths.ensure_file_exists(path, mode=0o600)

            assert "Cannot create file " in str(excinfo.value)
            mock_os_chmod.assert_called_once_with(path, 0o600)

    def test_get_permissions(self, mocker: MockFixture) -> None:
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        path = os.path.join(fake_dir, "tester.log")

        logger.info(f"path: {path}")

        paths.ensure_file_exists(path, mode=0o600)

        assert paths.get_permissions(path) == oct(384)  # same as 0o600

        os.unlink(path)
        shutil.rmtree(base, ignore_errors=True)

    def test_enforce_file_permissions(self, mocker: MockFixture) -> None:
        # mock_os_chmod = mocker.patch.object(
        #     ultron8.paths.os, "chmod", side_effect=IOError, autospec=True
        # )

        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        path = os.path.join(fake_dir, "tester.log")

        logger.info(f"path: {path}")

        paths.ensure_file_exists(path, mode=0o600)

        # change file permissions on purpose
        os.chmod(path, 0o644)

        with pytest.raises(Exception) as excinfo:
            paths.enforce_file_permissions(path)

            assert "File must only be accessible by owner. " in str(excinfo.value)
            # mock_os_chmod.assert_called_once_with(path, 0o600)

        os.unlink(path)
        shutil.rmtree(base, ignore_errors=True)

    def test_enforce_file_permissions_file_does_not_exist(
        self, mocker: MockFixture
    ) -> None:
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        path = os.path.join(fake_dir, "tester.log")

        # Don't create actual file on purpose

        with pytest.raises(Exception) as excinfo:
            paths.enforce_file_permissions(path)

            assert f"Path [{path}] is not a file" in str(excinfo.value)

        shutil.rmtree(base, ignore_errors=True)

    # def test_unicode_decode_error_isWritable(self, mocker):

    #     # mock
    #     mock_os_path_isdir = mocker.MagicMock(name="mock_os_path_isdir")
    #     mock_os_access = mocker.MagicMock(name="mock_os_access")
    #     mock_unicode_error_dialog = mocker.MagicMock(
    #         name="mock_unicode_error_dialog"
    #     )
    #     mock_logger_error = mocker.MagicMock(name="mock_logger_error")

    #     # patch
    #     mocker.patch.object(
    #         ultron8.paths.os.path, "isdir", mock_os_path_isdir
    #     )
    #     mocker.patch.object(
    #         ultron8.paths.os, "access", mock_os_access
    #     )
    #     mocker.patch.object(
    #         ultron8.paths, "unicode_error_dialog", mock_unicode_error_dialog
    #     )
    #     mocker.patch.object(
    #         scarlett_os.subprocess.logging.Logger, "error", mock_logger_error
    #     )

    #     path = b"file:///tmp/fake_file"

    #     # patch return values
    #     mock_os_path_isdir.side_effect = UnicodeDecodeError("", b"", 1, 0, "")
    #     paths.isWritable(path)

    #     assert mock_unicode_error_dialog.call_count == 1

    # def test_unicode_error_dialog(self, mocker):
    #     # mock
    #     mock_logger_error = mocker.MagicMock(name="mock_logger_error")
    #     # patch
    #     mocker.patch.object(
    #         scarlett_os.subprocess.logging.Logger, "error", mock_logger_error
    #     )

    #     paths.unicode_error_dialog()

    #     assert mock_logger_error.call_count == 1

    #     _message = _(
    #         "The system's locale that you are using is not UTF-8 capable. "
    #         "Unicode support is required for Python3 software like Pitivi. "
    #         "Please correct your system settings; if you try to use Pitivi "
    #         "with a broken locale, weird bugs will happen."
    #     )

    #     mock_logger_error.assert_any_call(_message)

    def test_path_to_uri(self) -> None:
        result = paths.path_to_uri("/etc/fstab")
        assert result == b"file:///etc/fstab"
        assert type(result) == bytes

    # def test_uri_is_valid_bytes(self):
    #     # uri = b"file:///etc/fstab"

    #     base = tempfile.mkdtemp()
    #     fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
    #     full_file_name = "fake"
    #     path = os.path.join(fake_dir, full_file_name)

    #     example_data = "test data"

    #     try:
    #         with open(path, "wt") as f:
    #             f.write(example_data)

    #         uri = paths.path_to_uri(path)
    #         assert paths.uri_is_valid(uri)

    #     finally:
    #         os.unlink(path)
    #         shutil.rmtree(base, ignore_errors=True)

    def test_path_from_uri_bytes(self) -> None:
        raw_uri = b"file:///etc/fstab"
        result = paths.path_from_uri(raw_uri)
        assert result == "/etc/fstab"

    def test_filename_from_uri_bytes(self) -> None:
        uri = b"file:///etc/fstab"
        result = paths.filename_from_uri(uri)
        assert result == "fstab"

    def test_filename_from_uri_str(self) -> None:
        uri = "file:///etc/fstab"
        result = paths.filename_from_uri(uri)
        assert result == "fstab"

    def test_quote_uri_byte_to_str(self) -> None:
        uri = b"file:///etc/fstab"
        result = paths.quote_uri(uri)
        assert result == "file:///etc/fstab"
        assert type(result) == str

    def test_quantize(self) -> None:
        result = paths.quantize(100.00, 3.00)
        assert result == 99.0

    def test_binary_search_EmptyList(self) -> None:
        assert paths.binary_search([], 10) == -1

    def test_binary_search_Existing(self) -> None:
        A = [10, 20, 30]
        for index, element in enumerate(A):
            assert paths.binary_search([10, 20, 30], element) == index

    def test_binary_search_MissingLeft(self) -> None:
        assert paths.binary_search([10, 20, 30], 1) == 0
        assert paths.binary_search([10, 20, 30], 16) == 1
        assert paths.binary_search([10, 20, 30], 29) == 2

    def test_binary_search_MissingRight(self) -> None:
        assert paths.binary_search([10, 20, 30], 11) == 0
        assert paths.binary_search([10, 20, 30], 24) == 1
        assert paths.binary_search([10, 20, 30], 40) == 2

    def test_uri_to_path_str(self) -> None:
        uri = "file:///etc/fstab"
        result = paths.uri_to_path(uri)
        assert result == "/etc/fstab"

    def test_uri_to_path_bytes(self) -> None:
        uri = b"file:///etc/fstab"
        result = paths.uri_to_path(uri)
        assert result == "/etc/fstab"

    def test_is_pathname_valid(self, mocker: MockFixture) -> None:
        assert paths.is_pathname_valid("foo.bar")
        # Long path valid?
        assert not paths.is_pathname_valid("a" * 256)
        assert not paths.is_pathname_valid(None)

    def test_is_path_creatable(self, mocker: MockFixture) -> None:
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        full_file_name = "fake"
        path = os.path.join(fake_dir, full_file_name)

        assert paths.is_path_creatable(path)
        assert not paths.is_path_creatable("/bossjones/is/the/best/file.txt")

        shutil.rmtree(base, ignore_errors=True)

    def test_is_path_exists_or_creatable(self, mocker: MockFixture) -> None:
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        full_file_name = "fake"
        path = os.path.join(fake_dir, full_file_name)

        assert paths.is_path_exists_or_creatable(path)

        assert not paths.is_path_exists_or_creatable("/bossjones/is/the/best/file.txt")

        shutil.rmtree(base, ignore_errors=True)

    def test_is_path_sibling_creatable(self, mocker: MockFixture) -> None:
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        full_file_name = "fake"
        path = os.path.join(fake_dir, full_file_name)

        assert paths.is_path_sibling_creatable(path)

        assert not paths.is_path_sibling_creatable("/bossjones/is/the/best/file.txt")

        shutil.rmtree(base, ignore_errors=True)

    def test_is_path_exists_or_creatable_portable(self, mocker: MockFixture) -> None:
        base = tempfile.mkdtemp()
        fake_dir = tempfile.mkdtemp(prefix="config", dir=base)
        full_file_name = "fake"
        path = os.path.join(fake_dir, full_file_name)

        assert paths.is_path_exists_or_creatable_portable(path)

        assert not paths.is_path_exists_or_creatable_portable(
            "/bossjones/is/the/best/file.txt"
        )

        shutil.rmtree(base, ignore_errors=True)


##################################################################################
# Pitivi - BEGIN
##################################################################################
# def testMakeBackupUri(self):
#     uri = "file:///tmp/x.xges"
#     self.assertEqual(uri + "~", self.manager._makeBackupURI(uri))
#
# def testBackupProject(self):
#     self.manager.newBlankProject()
#
#     # Assign an uri to the project where it's saved by default.
#     unused, xges_path = tempfile.mkstemp(suffix=".xges")
#     uri = "file://" + os.path.abspath(xges_path)
#     self.manager.current_project.uri = uri
#     # This is where the automatic backup file is saved.
#     backup_uri = self.manager._makeBackupURI(uri)
#
#     # Save the backup
#     self.assertTrue(self.manager.saveProject(
#         self.manager.current_project, backup=True))
#     self.assertTrue(os.path.isfile(path_from_uri(backup_uri)))
#
#     self.manager.closeRunningProject()
#     self.assertFalse(os.path.isfile(path_from_uri(backup_uri)),
#                      "Backup file not deleted when project closed")
##################################################################################
# Pitivi - BEGIN
##################################################################################

#     def test_space_in_path(self):
#         result = path.path_to_uri('/tmp/test this')
#         self.assertEqual(result, 'file:///tmp/test%20this')
#
#     def test_unicode_in_path(self):
#         result = path.path_to_uri('/tmp/æøå')
#         self.assertEqual(result, 'file:///tmp/%C3%A6%C3%B8%C3%A5')
#
#     def test_utf8_in_path(self):
#         result = path.path_to_uri('/tmp/æøå'.encode('utf-8'))
#         self.assertEqual(result, 'file:///tmp/%C3%A6%C3%B8%C3%A5')
#
#     def test_latin1_in_path(self):
#         result = path.path_to_uri('/tmp/æøå'.encode('latin-1'))
#         self.assertEqual(result, 'file:///tmp/%E6%F8%E5')
#
#
# class UriToPathTest(unittest.TestCase):
#
#     def test_simple_uri(self):
#         result = path.uri_to_path('file:///etc/fstab')
#         self.assertEqual(result, '/etc/fstab'.encode('utf-8'))
#
#     def test_space_in_uri(self):
#         result = path.uri_to_path('file:///tmp/test%20this')
#         self.assertEqual(result, '/tmp/test this'.encode('utf-8'))
#
#     def test_unicode_in_uri(self):
#         result = path.uri_to_path('file:///tmp/%C3%A6%C3%B8%C3%A5')
#         self.assertEqual(result, '/tmp/æøå'.encode('utf-8'))
#
#     def test_latin1_in_uri(self):
#         result = path.uri_to_path('file:///tmp/%E6%F8%E5')
#         self.assertEqual(result, '/tmp/æøå'.encode('latin-1'))
#
#
# class SplitPathTest(unittest.TestCase):
#
#     def test_empty_path(self):
#         self.assertEqual([], path.split_path(''))
#
#     def test_single_dir(self):
#         self.assertEqual(['foo'], path.split_path('foo'))
#
#     def test_dirs(self):
#         self.assertEqual(['foo', 'bar', 'baz'], path.split_path('foo/bar/baz'))
#
#     def test_initial_slash_is_ignored(self):
#         self.assertEqual(
#             ['foo', 'bar', 'baz'], path.split_path('/foo/bar/baz'))
#
#     def test_only_slash(self):
#         self.assertEqual([], path.split_path('/'))
#
#
# class FindMTimesTest(unittest.TestCase):
#     maxDiff = None
#
#     def setUp(self):  # noqa: N802
#         self.tmpdir = tempfile.mkdtemp(b'.scarlett_os-tests')
#
#     def tearDown(self):  # noqa: N802
#         shutil.rmtree(self.tmpdir, ignore_errors=True)
#
#     def mkdir(self, *args):
#         name = os.path.join(self.tmpdir, *[bytes(a) for a in args])
#         os.mkdir(name)
#         return name
#
#     def touch(self, *args):
#         name = os.path.join(self.tmpdir, *[bytes(a) for a in args])
#         open(name, 'w').close()
#         return name
#
#     def test_names_are_bytestrings(self):
#         """We shouldn't be mixing in unicode for paths."""
#         result, errors = path.find_mtimes(tests.path_to_data_dir(''))
#         for name in list(result.keys()) + list(errors.keys()):
#             self.assertEqual(name, tests.IsA(bytes))
#
#     def test_nonexistent_dir(self):
#         """Non existent search roots are an error"""
#         missing = os.path.join(self.tmpdir, 'does-not-exist')
#         result, errors = path.find_mtimes(missing)
#         self.assertEqual(result, {})
#         self.assertEqual(errors, {missing: tests.IsA(exceptions.FindError)})
#
#     def test_empty_dir(self):
#         """Empty directories should not show up in results"""
#         self.mkdir('empty')
#
#         result, errors = path.find_mtimes(self.tmpdir)
#         self.assertEqual(result, {})
#         self.assertEqual(errors, {})
#
#     def test_file_as_the_root(self):
#         """Specifying a file as the root should just return the file"""
#         single = self.touch('single')
#
#         result, errors = path.find_mtimes(single)
#         self.assertEqual(result, {single: tests.any_int})
#         self.assertEqual(errors, {})
#
#     def test_nested_directories(self):
#         """Searching nested directories should find all files"""
#
#         # Setup foo/bar and baz directories
#         self.mkdir('foo')
#         self.mkdir('foo', 'bar')
#         self.mkdir('baz')
#
#         # Touch foo/file foo/bar/file and baz/file
#         foo_file = self.touch('foo', 'file')
#         foo_bar_file = self.touch('foo', 'bar', 'file')
#         baz_file = self.touch('baz', 'file')
#
#         result, errors = path.find_mtimes(self.tmpdir)
#         self.assertEqual(result, {foo_file: tests.any_int,
#                                   foo_bar_file: tests.any_int,
#                                   baz_file: tests.any_int})
#         self.assertEqual(errors, {})
#
#     def test_missing_permission_to_file(self):
#         """Missing permissions to a file is not a search error"""
#         target = self.touch('no-permission')
#         os.chmod(target, 0)
#
#         result, errors = path.find_mtimes(self.tmpdir)
#         self.assertEqual({target: tests.any_int}, result)
#         self.assertEqual({}, errors)
#
#     def test_missing_permission_to_directory(self):
#         """Missing permissions to a directory is an error"""
#         directory = self.mkdir('no-permission')
#         os.chmod(directory, 0)
#
#         result, errors = path.find_mtimes(self.tmpdir)
#         self.assertEqual({}, result)
#         self.assertEqual({directory: tests.IsA(exceptions.FindError)}, errors)
#
#     def test_symlinks_are_ignored(self):
#         """By default symlinks should be treated as an error"""
#         target = self.touch('target')
#         link = os.path.join(self.tmpdir, 'link')
#         os.symlink(target, link)
#
#         result, errors = path.find_mtimes(self.tmpdir)
#         self.assertEqual(result, {target: tests.any_int})
#         self.assertEqual(errors, {link: tests.IsA(exceptions.FindError)})
#
#     def test_symlink_to_file_as_root_is_followed(self):
#         """Passing a symlink as the root should be followed when follow=True"""
#         target = self.touch('target')
#         link = os.path.join(self.tmpdir, 'link')
#         os.symlink(target, link)
#
#         result, errors = path.find_mtimes(link, follow=True)
#         self.assertEqual({link: tests.any_int}, result)
#         self.assertEqual({}, errors)
#
#     def test_symlink_to_directory_is_followed(self):
#         pass
#
#     def test_symlink_pointing_at_itself_fails(self):
#         """Symlink pointing at itself should give as an OS error"""
#         link = os.path.join(self.tmpdir, 'link')
#         os.symlink(link, link)
#
#         result, errors = path.find_mtimes(link, follow=True)
#         self.assertEqual({}, result)
#         self.assertEqual({link: tests.IsA(exceptions.FindError)}, errors)
#
#     def test_symlink_pointing_at_parent_fails(self):
#         """We should detect a loop via the parent and give up on the branch"""
#         os.symlink(self.tmpdir, os.path.join(self.tmpdir, 'link'))
#
#         result, errors = path.find_mtimes(self.tmpdir, follow=True)
#         self.assertEqual({}, result)
#         self.assertEqual(1, len(errors))
#         self.assertEqual(tests.IsA(Exception), list(errors.values())[0])
#
#     def test_indirect_symlink_loop(self):
#         """More indirect loops should also be detected"""
#         # Setup tmpdir/directory/loop where loop points to tmpdir
#         directory = os.path.join(self.tmpdir, b'directory')
#         loop = os.path.join(directory, b'loop')
#
#         os.mkdir(directory)
#         os.symlink(self.tmpdir, loop)
#
#         result, errors = path.find_mtimes(self.tmpdir, follow=True)
#         self.assertEqual({}, result)
#         self.assertEqual({loop: tests.IsA(Exception)}, errors)
#
#     def test_symlink_branches_are_not_excluded(self):
#         """Using symlinks to make a file show up multiple times should work"""
#         self.mkdir('directory')
#         target = self.touch('directory', 'target')
#         link1 = os.path.join(self.tmpdir, b'link1')
#         link2 = os.path.join(self.tmpdir, b'link2')
#
#         os.symlink(target, link1)
#         os.symlink(target, link2)
#
#         expected = {target: tests.any_int,
#                     link1: tests.any_int,
#                     link2: tests.any_int}
#
#         result, errors = path.find_mtimes(self.tmpdir, follow=True)
#         self.assertEqual(expected, result)
#         self.assertEqual({}, errors)
#
#     def test_gives_mtime_in_milliseconds(self):
#         fname = self.touch('foobar')
#
#         os.utime(fname, (1, 3.14159265))
#
#         result, errors = path.find_mtimes(fname)
#
#         self.assertEqual(len(result), 1)
#         mtime, = list(result.values())
#         self.assertEqual(mtime, 3141)
#         self.assertEqual(errors, {})
#
#
# class TestIsPathInsideBaseDir(object):
#     def test_when_inside(self):
#         assert path.is_path_inside_base_dir(
#             '/æ/øå'.encode('utf-8'),
#             '/æ'.encode('utf-8'))
#
#     def test_when_outside(self):
#         assert not path.is_path_inside_base_dir(
#             '/æ/øå'.encode('utf-8'),
#             '/ø'.encode('utf-8'))
#
#     def test_byte_inside_str_fails(self):
#         with pytest.raises(ValueError):
#             path.is_path_inside_base_dir('/æ/øå'.encode('utf-8'), '/æ')
#
#     def test_str_inside_byte_fails(self):
#         with pytest.raises(ValueError):
#             path.is_path_inside_base_dir('/æ/øå', '/æ'.encode('utf-8'))
#
#     def test_str_inside_str_fails(self):
#         with pytest.raises(ValueError):
#             path.is_path_inside_base_dir('/æ/øå', '/æ')
#
#
# # TODO: kill this in favour of just os.path.getmtime + mocks
# class MtimeTest(unittest.TestCase):
#
#     def tearDown(self):  # noqa: N802
#         path.mtime.undo_fake()
#
#     def test_mtime_of_current_dir(self):
#         mtime_dir = int(os.stat('.').st_mtime)
#         self.assertEqual(mtime_dir, path.mtime('.'))
#
#     def test_fake_time_is_returned(self):
#         path.mtime.set_fake_time(123456)
#         self.assertEqual(path.mtime('.'), 123456)
