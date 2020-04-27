import sys
import os
import shutil
import pathlib
import stat
from pathlib import Path
from dataclasses import dataclass
from typing import Deque, Dict, List

from ultron8.logging_init import getLogger
from ultron8.core.files import write_file

from ultron8.config import get_config_dir_base_path
from ultron8.paths import is_readable_dir, ensure_dir_exists, is_readable_file, tree

from ultron8.config.base import config_dirs, CONFIG_FILENAME

from ultron8.config import ConfigManager

logger = getLogger(__name__)


# ################################################################################
# # https://github.com/martin2250/linux-common/blob/61892f720c77eb0ac5ff3381f8ab62660bd254ce/bin/syncmp3lib
# @dataclass
# class FileInfo:
#     stat: os.stat_result
#     path: pathlib.Path = None
#     path_rel: pathlib.Path = None

#     def is_file(self):
#         return stat.S_ISREG(self.stat.st_mode)

#     def is_dir(self):
#         return stat.S_ISDIR(self.stat.st_mode)

#     def size(self):
#         return self.stat.st_size

#     def mtime(self):
#         return self.stat.st_mtime


# def scan(path: pathlib.PurePath):
#     """Scan a path for files and empty directories"""

#     path = pathlib.Path(path)

#     for directory_name, dir_names, file_names in os.walk(path):
#         print(f" For {path} | directory_name={directory_name}, dir_names={dir_names}, file_names={file_names}")
#         for file_name in file_names:
#             child = path / pathlib.Path(os.path.join(directory_name, file_name))
#             info = FileInfo(os.lstat(child), child, child.relative_to(path))
#             yield info

#         # if directory does not have any sub folders, or any files in it
#         if not (dir_names or file_names):
#             child = path / pathlib.Path(directory_name)
#             info = FileInfo(os.lstat(child), child, child.relative_to(path))
#             yield info


# def scan_path(
#     files: List[FileInfo],
#     dirs: List[FileInfo],
#     path: pathlib.PurePath):
#     """Scan path, append all files to files and all empty folders to dirs"""

#     for info in scan(path):
#         if info.is_file():
#             files.append(info)
#         elif info.is_dir():
#             dirs.append(info)


# def check_directory_exists(path):
#     path = pathlib.Path(path).resolve()
#     if not path.is_dir():
#         print(f'directory {path} does not exist!')
#     else:
#         return path

# def dont_check_directory_exists(path):
#     path = pathlib.Path(path).resolve()
#     return path

# def check_file_exists(path):
#     path = pathlib.Path(path).resolve()
#     if not path.is_file():
#         print(f'file {path} does not exist!')
#     else:
#         return path


# def delete_checkdir(path: pathlib.PurePath):
#     """delete file or directory, also delete parent directories if they are empty"""
#     while True:
#         if path.is_file():
#             path.unlink()
#         else:
#             path.rmdir()
#         path = path.parent
#         if os.listdir(path):
#             break

# ################################################################################


def app_home():
    app_base_dir = config_dirs()[0]
    return os.path.join(app_base_dir, "ultron8")


def cluster_home():
    return os.path.join(app_home(), "clusters")


def workspace_home():
    return os.path.join(app_home(), "workspace")


def libs_home():
    return os.path.join(app_home(), "libs")


def mkdir_if_dne(target):
    res = is_readable_dir(target)
    if not res["result"]:
        logger.debug(
            "[{}] | {} does not exist, creating .... ".format(
                sys._getframe().f_code.co_name, target
            )
        )
        ensure_dir_exists(target)


def str_to_path(path):
    path = pathlib.Path(path).resolve()
    return path


def prep_default_config():
    cm = ConfigManager()
    home = app_home()
    res = is_readable_dir(home)
    if not res["result"]:
        logger.debug(
            "[{}] | {} does not exist, creating .... ".format(
                sys._getframe().f_code.co_name, home
            )
        )
        ensure_dir_exists(home)
    default_cfg = cm.get_cfg_file_path()

    res = is_readable_file(default_cfg)

    if not res["result"]:
        logger.debug(
            "[{}] | {} does not exist, creating .... ".format(
                sys._getframe().f_code.co_name, default_cfg
            )
        )
        # write empty file first
        file = open(default_cfg, "w")
        file.write("{}")
        file.close()

        cm.save()
    return default_cfg


# INFO: https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Metaprogramming.html#intercepting-class-creation
# # Metaprogramming/Singleton.py

# class Singleton(type):
#     instance = None
#     def __call__(cls, *args, **kw):
#         if not cls.instance:
#              cls.instance = super(Singleton, cls).__call__(*args, **kw)
#         return cls.instance

# class ASingleton(object):
#     __metaclass__ = Singleton

# class WorkspaceBase:
#     def __init__(self, wdir=None, libdir=None, **kwargs):
#         super().__init__(**kwargs)
#         self._wdir = wdir
#         self._lib_dir = libdir

#     def clean(self):
#         pass

#     def set_dir(self, d):
#         pass

#     def copy_libs(self):
#         pass

#     def copy_templates(self, in_dir):
#         """
#         copy over lib files, and THEN user files to ensure overwrites
#         """
#         pass

#     def copy_contents(self, source, subdir="", sourcedir=None):
#         pass

#     def create_subdir(self, subdir):
#         pass

#     def write_template(self, path, contents):
#         pass

#     def template_subdir(self):
#         pass

#     def _default_workspace(self):
#         pass

#     def _default_libdir(self):
#         pass


class CliWorkspace:
    # @classmethod
    # def from_configmanager(cls, cm):
    #     workspace_dir = os.path.join(cm.get_config_dir(), "workspace")
    #     libs_dir = os.path.join(cm.get_config_dir(), "libs")
    #     kwargs = dict(wdir=workspace_dir, libdir=libs_dir,)
    #     return cls(**kwargs)

    def __init__(
        self, wdir=None, libdir=None, setup=False, ignore_errors=False, create=True
    ):
        self._wdir = wdir
        self._lib_dir = libdir
        self._template_dir = None
        self.api = None
        self._root = self._default_root()
        self._setup_api()

        self._setup = False

        if setup:
            self.setup(ignore_errors, create)

    def setup(self, ignore_errors=False, create=True):
        self.configure()
        self.verify(ignore_errors, create)
        self._setup = True

    def _setup_api(self):
        self.api = str_to_path(self._root)

    # initialize all values
    def configure(self):
        if self._wdir is None:
            self._wdir = self._default_workspace()
        if self._lib_dir is None:
            self._lib_dir = self._default_libdir()
        if self._template_dir is None:
            self._template_dir = self._default_templates()

    def tree(self):
        tree(self.api.cwd())

    def create_default_config(self):
        prep_default_config()

    # def setup(self, wdir=None, libdir=None):
    #     self._wdir = None
    #     if wdir is None:
    #         wdir = self._default_workspace()
    #     self.set_dir(wdir)
    #     self._lib_dir = None
    #     if libdir is None:
    #         libdir = self._default_libdir()
    #     mkdir_if_dne(libdir)
    #     self._lib_dir = libdir

    def verify(self, ignore_errors=False, create=True):
        list_to_verify = self.check()
        if create:
            for i in list_to_verify:
                if i["kind"] is "d":
                    temp_dir = os.path.join(self._root, i["key"])
                    mkdir_if_dne(temp_dir)
            # Re-Run check to get latest values
            self.create_default_config()
            list_to_verify = self.check()

        if ignore_errors:
            return

        for i in list_to_verify:
            assert i["value"]
            # for v in i.values():
            #     assert v

    def build_whitelist_dirs(self):
        whitelist_dirs = dict()
        # whitelist_dirs["root"] = self.api
        whitelist_dirs["workspace"] = self.api.joinpath("workspace")
        whitelist_dirs["templates"] = self.api.joinpath("templates")
        whitelist_dirs["libs"] = self.api.joinpath("libs")
        return whitelist_dirs

    def build_whitelist_files(self):
        whitelist_files = dict()
        whitelist_files["cfg_file"] = self.api.joinpath("smart.yaml")
        return whitelist_files

    def check(self):
        whitelist_dirs = self.build_whitelist_dirs()
        checked = []
        for k, v in whitelist_dirs.items():
            checked.append({"key": str(k), "value": self._check_dir(v), "kind": "d"})
        whitelist_files = self.build_whitelist_files()
        for k, v in whitelist_files.items():
            checked.append({"key": str(k), "value": self._check_file(v), "kind": "f"})
        return checked

    def _check_dir(self, p):
        return p.is_dir()

    def _check_file(self, f):
        return f.is_file()

    # def clean(self):
    #     logger.debug(
    #         "[{}] | removing dir tree starting at {} .... ".format(
    #             sys._getframe().f_code.co_name, self._wdir
    #         )
    #     )
    #     shutil.rmtree(self._wdir)
    #     self.set_dir(self._wdir)

    # def set_dir(self, d):
    #     """
    #     Sets the directory that this object is tied to. If the
    #     directory given actually is different, the contents will be
    #     copied over
    #     """
    #     mkdir_if_dne(d)
    #     old_workspace = self._wdir
    #     self._wdir = d
    #     if not d == old_workspace and old_workspace is not None:
    #         logger.debug(
    #             "[{}] | copying contents from {} to {} .... ".format(
    #                 sys._getframe().f_code.co_name, old_workspace, self._wdir
    #             )
    #         )
    #         self.copy_contents(old_workspace)

    # def copy_libs(self):
    #     self.copy_contents(self._lib_dir, subdir=os.path.join("templates", "libs"))

    # def copy_templates(self, in_dir):
    #     """
    #     copy over lib files, and THEN user files to ensure overwrites
    #     """
    #     self.copy_contents(in_dir, subdir="templates")

    # def copy_contents(self, source, subdir="", sourcedir=None):
    #     if sourcedir is None:
    #         sourcedir = self._wdir
    #     subdir_fp = os.path.join(sourcedir, subdir)
    #     mkdir_if_dne(subdir_fp)
    #     if os.path.isfile(source) and not os.path.isdir(source):
    #         shutil.copy(source, subdir_fp)
    #         return
    #     # because shutil.copytree fails when sourcedir exists and
    #     # is given as the destination
    #     for fi in os.listdir(source):
    #         fpath = os.path.join(source, fi)
    #         # listed dir IS the target dir - skip to prevent infinite recursion
    #         if fpath in os.path.join(sourcedir, fi):
    #             continue
    #         if os.path.isdir(fpath):
    #             shutil.copytree(fpath, os.path.join(subdir_fp, fi))
    #             continue
    #         shutil.copy(fpath, subdir_fp)

    # def create_subdir(self, subdir):
    #     full_path = os.path.join(self._wdir, subdir)
    #     if os.path.isdir(full_path):
    #         return
    #     os.mkdir(full_path)

    # def write_template(self, path, contents):
    #     write_file(os.path.join(self._wdir, path), contents, mode="a")

    # def template_subdir(self):
    #     return os.path.join(self._wdir, "templates")

    def _default_clusters(self):
        return os.path.join(app_home(), "clusters")

    def _default_templates(self):
        return os.path.join(app_home(), "templates")

    def _default_workspace(self):
        return workspace_home()

    def _default_libdir(self):
        return libs_home()

    def _default_root(self):
        return app_home()

    # def get_workdir(self):
    #     return self._wdir
