from __future__ import absolute_import
from ultron8.exceptions import UltronBaseException
from ultron8.exceptions import UltronPluginException


class SensorPluginException(UltronPluginException):
    pass


class TriggerTypeRegistrationException(SensorPluginException):
    pass


class SensorNotFoundException(UltronBaseException):
    pass


class SensorPartitionerNotSupportedException(UltronBaseException):
    pass


class SensorPartitionMapMissingException(UltronBaseException):
    pass
