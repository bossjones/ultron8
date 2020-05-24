from __future__ import absolute_import

from ultron8.exceptions import UltronPluginException


class PluginLoadError(UltronPluginException):
    pass


class IncompatiblePluginException(UltronPluginException):
    pass
