import os
import shutil

from ultron8.logging_init import getLogger
from ultron8.core.files import write_file

logger = getLogger(__name__)


def app_home():
    try:
        return os.path.join(os.environ["HOME"], ".ultron8")
    except KeyError:
        raise "HOME environment variable not set?"


def cluster_home():
    try:
        return os.path.join(app_home(), "clusters")
    except KeyError:
        raise "HOME environment variable not set?"


def mkdir_if_dne(target):
    if not os.path.isdir(target):
        os.makedirs(target)


def prep_default_config():
    home = app_home()
    if not os.path.exists(home):
        os.makedirs(home)
    default_cfg = os.path.join(home, "config.json")
    if not os.path.exists(default_cfg):
        file = open(default_cfg, "w")
        file.write("{}")
        file.close()
    return default_cfg


class Workspace:
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
        return os.path.join(app_home(), "workspace")

    def _default_libdir(self):
        return os.path.join(app_home(), "libs")
