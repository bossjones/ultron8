from pathlib import Path
import os


class Paths(object):
    @property
    def base_path_dir(self):
        return Path("/".join((os.path.expanduser("~"))))

    @property
    def ultron_config_dir(self):
        return self.base_path_dir / ".config" / "ultron8"

    @property
    def ultron_config_path_file(self):
        return self.ultron_config_dir / "config.yaml"

    @property
    def here_path_dir(self):
        return Path(os.path.join(os.path.dirname(os.path.abspath(__file__))))

    @property
    def default_config_path_file(self):
        return self.here_path_dir / "default_config.yaml"

    @property
    def data_home_path_dir(self):
        return self.base_path_dir / ".local" / "share" / "ultron8" / "data"

    @property
    def build_path_dir(self):
        return self.base_path_dir / ".local" / "share" / "ultron8" / "build"

    @property
    def cache_home_dir(self):
        return self.base_path_dir / ".cache" / "ultron8"

    # @property
    # def assets_path(self):
    #     return self.base_path_dir / 'assets'

    # @property
    # def template_path(self):
    #     return self.base_path_dir / 'template'
