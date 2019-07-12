"""
Data Models for all things having to do with Sensors.
"""
from datetime import datetime
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import Union

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Schema

from ultron8.api.models.trigger import TriggerTypeBase
from ultron8.api.models.trigger import TriggerTypeBaseDB

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


class ParametersSchemaBase(BaseModel):
    type: str
    # properties: Union[FilePathModel, HostInfoModel]
    properties: dict = {}
    additionalProperties: bool


class ParametersSchemaBaseDB(ParametersSchemaBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None


class SensorsBase(BaseModel):
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
    class_name: Optional[str] = None
    enabled: Optional[bool] = True
    entry_point: Optional[str] = None  # eg. "checks/check_loadavg.py"
    description: Optional[str] = None
    trigger_types: Optional[List[TriggerTypeBase]] = []
    # created_at: datetime = None
    # updated_at: datetime = None
    # deleted_at: datetime = None


class SensorsBaseInDB(SensorsBase):
    id: int
    ref: str
    packs_id: int
    created_at: datetime = None
    updated_at: datetime = None


class SensorsCreate(SensorsBaseInDB):
    class_name: Optional[str] = None
    enabled: Optional[bool] = None
    entry_point: Optional[str] = None  # eg. "checks/check_loadavg.py"
    description: Optional[str] = None
    trigger_types: Optional[List[TriggerTypeBase]] = []


class SensorsUpdate(SensorsBaseInDB):
    class_name: Optional[str] = None
    enabled: Optional[bool] = None
    entry_point: Optional[str] = None  # eg. "checks/check_loadavg.py"
    description: Optional[str] = None
    trigger_types: Optional[List[TriggerTypeBase]] = []


class Sensor(SensorsBaseInDB):
    pass


class SensorInDb(SensorsBaseInDB):
    pass


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

    sensor = SensorsBase(**external_data)
    print(sensor)

    print(sensor.class_name)
