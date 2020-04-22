import os
import shutil

from ultron8.logging_init import getLogger
from ultron8.core.files import write_file

from ultron8.config import get_config_dir_base_path
from ultron8.paths import is_readable_dir, ensure_dir_exists

from ultron8.config.base import config_dirs, CONFIG_FILENAME

logger = getLogger(__name__)


def app_home():
    app_base_dir = config_dirs()[0]
    return os.path.join(app_base_dir, "ultron8")


def cluster_home():
    return os.path.join(app_home(), "clusters")


def mkdir_if_dne(target):
    res = is_readable_dir(target)
    if not res["result"]:
        ensure_dir_exists(target)


def prep_default_config():
    home = app_home()
    if not os.path.exists(home):
        os.makedirs(home)
    default_cfg = os.path.join(home, CONFIG_FILENAME)
    if not os.path.exists(default_cfg):
        file = open(default_cfg, "w")
        file.write("{}")
        file.close()
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
    def __init__(self, wdir=None, libdir=None):
        self._wdir = None
        if wdir is None:
            wdir = self._default_workspace()
        self.set_dir(wdir)
        self._lib_dir = None
        if libdir is None:
            libdir = self._default_libdir()
        mkdir_if_dne(libdir)
        self._lib_dir = libdir

    def clean(self):
        shutil.rmtree(self._wdir)
        self.set_dir(self._wdir)

    def set_dir(self, d):
        """
        Sets the directory that this object is tied to. If the
        directory given actually is different, the contents will be
        copied over
        """
        mkdir_if_dne(d)
        old_workspace = self._wdir
        self._wdir = d
        if not d == old_workspace and old_workspace is not None:
            self.copy_contents(old_workspace)

    def copy_libs(self):
        self.copy_contents(self._lib_dir, subdir=os.path.join("templates", "libs"))

    def copy_templates(self, in_dir):
        """
        copy over lib files, and THEN user files to ensure overwrites
        """
        self.copy_contents(in_dir, subdir="templates")

    def copy_contents(self, source, subdir="", sourcedir=None):
        if sourcedir is None:
            sourcedir = self._wdir
        subdir_fp = os.path.join(sourcedir, subdir)
        mkdir_if_dne(subdir_fp)
        if os.path.isfile(source) and not os.path.isdir(source):
            shutil.copy(source, subdir_fp)
            return
        # because shutil.copytree fails when sourcedir exists and
        # is given as the destination
        for fi in os.listdir(source):
            fpath = os.path.join(source, fi)
            # listed dir IS the target dir - skip to prevent infinite recursion
            if fpath in os.path.join(sourcedir, fi):
                continue
            if os.path.isdir(fpath):
                shutil.copytree(fpath, os.path.join(subdir_fp, fi))
                continue
            shutil.copy(fpath, subdir_fp)

    def create_subdir(self, subdir):
        full_path = os.path.join(self._wdir, subdir)
        if os.path.isdir(full_path):
            return
        os.mkdir(full_path)

    def write_template(self, path, contents):
        write_file(os.path.join(self._wdir, path), contents, mode="a")

    def template_subdir(self):
        return os.path.join(self._wdir, "templates")

    def _default_workspace(self):
        return os.path.join(get_config_dir_base_path(), ".ultron8", "workspace")

    def _default_libdir(self):
        return os.path.join(get_config_dir_base_path(), ".ultron8", "libs")
