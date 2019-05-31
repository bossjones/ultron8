from pathlib import Path
import os


class Paths(object):
    @property
    def ultron_config_path(self):
        return Path("/".join((os.path.expanduser("~"), ".config", "ultron8", "config.yaml")))

    @property
    def default_config_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "default_config.yaml")

    # @property
    # def assets_path(self):
    #     return self.ultron_path / 'assets'

    # @property
    # def build_path(self):
    #     return self.ultron_path / 'build'

    # @property
    # def template_path(self):
    #     return self.ultron_path / 'template'
