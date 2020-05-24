"""
Data Models for all things having to do with Sensors.
"""
from datetime import datetime
from enum import Enum

from typing import Dict, List, Optional, Sequence, Set, Tuple, Union

from pydantic import BaseModel, Schema

from ultron8.api.db_models.trigger import TriggerTypeDB
from ultron8.api.models.base import BaseDataModel
from ultron8.api.models.trigger import TriggerTypeInDBModel

# SOURCE: https://github.com/tiangolo/fastapi/issues/634
try:
    from pydantic import EmailStr
except ImportError:
    from pydantic.networks import EmailStr


# The ellipsis ... just means "Required" same as annotation only declarations above.


class SensorsBase(BaseDataModel):
    """Sensor Data Model.

    name: "SampleSensor"
    entry_point: "sample_sensor.py"
    description: "Sample sensor that emits triggers."
    trigger_types:
      -
        name: "event"
        description: "An example trigger."
        payload_schema:
          type: "object"
          properties:
            executed_at:
              type: "string"
              format: "date-time"
              default: "2014-07-30 05:04:24.578325"

    Arguments:
        BaseModel {[type]} -- [description]
    """

    id: Optional[int] = None
    class_name: Optional[str] = None
    packs_name: Optional[str] = None
    ref: Optional[str] = None
    uid: Optional[str] = None
    artifact_uri: Optional[str] = None
    poll_interval: Optional[str] = None
    enabled: Optional[bool] = True
    entry_point: Optional[str] = None  # eg. "checks/check_loadavg.py"
    description: Optional[str] = None
    trigger_types: Optional[List[TriggerTypeInDBModel]] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True


class SensorsBaseInDB(SensorsBase):
    id: int = None
    class_name: str
    packs_name: str
    ref: Optional[str] = None
    uid: Optional[str] = None
    artifact_uri: Optional[str] = None
    poll_interval: Optional[str] = None
    enabled: Optional[bool] = True
    entry_point: Optional[str] = None  # eg. "checks/check_loadavg.py"
    description: Optional[str] = ""
    trigger_types: Optional[List[TriggerTypeInDBModel]] = []


class SensorsCreate(SensorsBaseInDB):
    class_name: Optional[str] = None
    enabled: Optional[bool] = None
    entry_point: Optional[str] = None  # eg. "checks/check_loadavg.py"
    description: Optional[str] = None
    trigger_types: Optional[List[TriggerTypeInDBModel]] = []


class SensorsUpdate(SensorsBaseInDB):
    pass


class Sensor(SensorsBaseInDB):
    pass


class SensorInDB(SensorsBaseInDB):
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
