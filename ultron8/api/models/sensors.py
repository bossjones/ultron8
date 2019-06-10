"""
Data Models for all things having to do with Sensors.
"""

from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from enum import Enum
from pydantic import BaseModel, Schema, EmailStr
from datetime import datetime

# The ellipsis ... just means "Required" same as annotation only declarations above.


class LineModel(BaseModel):
    """
    File Line Model.
    """

    description: str = None
    type: str
    required: bool = None


class FileNameModel(BaseModel):
    description: str = None
    type: str
    required: bool = None


class FilePathModel(BaseModel):
    description: str = None
    type: str
    required: bool = None


class HostInfoModel(BaseModel):
    hostname: str = None


class ProcessInfoModel(BaseModel):
    hostname: str = None
    pid: int


class ParametersSchemaModel(BaseModel):
    # id: int
    type: str
    properties: Union[FilePathModel, HostInfoModel]
    additionalProperties: bool
    created_at: datetime = None
    updated_at: datetime = None
    deleted_at: datetime = None


class TriggerTypeBase(BaseModel):
    # id: int
    name: str
    description: str = None
    parameters_schema: ParametersSchemaModel = ...
    payload_schema: dict
    # created_at: datetime = None
    # updated_at: datetime = None
    # deleted_at: datetime = None


class SensorsModel(BaseModel):
    """Sensor Data Model.

    class_name: "FileWatchSensor"
    enabled: true
    entry_point: "file_watch_sensor.py"
    description: "Sensor which monitors files for new lines"
    trigger_types:
      -
        name: "file_watch.line"
        pack: "linux"
        description: "Trigger which indicates a new line has been detected"
        # This sensor can be supplied a path to a file to tail via a rule.
        parameters_schema:
          type: "object"
          properties:
            file_path:
              description: "Path to the file to monitor"
              type: "string"
              required: true
          additionalProperties: false
        # This is the schema of the trigger payload the sensor generates
        payload_schema:
          type: "object"
          properties:
            file_path:
              type: "string"
            file_name:
              type: "string"
            line:
              type: "string"

    Arguments:
        BaseModel {[type]} -- [description]
    """

    # id: int
    class_name: str
    enabled: bool
    entry_point: str  # eg. "checks/check_loadavg.py"
    description: str = None
    trigger_types: List[TriggerTypeBase] = []
    # created_at: datetime = None
    # updated_at: datetime = None
    # deleted_at: datetime = None


if "__main__" == __name__:
    # Self-referencing Model
    # SensorsModel.update_forward_refs()
    external_data = {
        "class_name": "FileWatchSensor",
        "enabled": True,
        "entry_point": "file_watch_sensor.py",
        "description": "Sensor which monitors files for new lines",
        "trigger_types": [
            {
                "name": "file_watch.line",
                "pack": "linux",
                "description": "Trigger which indicates a new line has been detected",
                "parameters_schema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "description": "Path to the file to monitor",
                            "type": "string",
                            "required": True,
                        }
                    },
                    "additionalProperties": False,
                },
                "payload_schema": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string"},
                        "file_name": {"type": "string"},
                        "line": {"type": "string"},
                    },
                },
            }
        ],
    }

    sensor = SensorsModel(**external_data)
    print(sensor)

    print(sensor.class_name)
