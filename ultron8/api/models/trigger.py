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
from pydantic import Schema


class TriggerTypeBase(BaseModel):
    name: str
    description: str = None
    # parameters_schema: ParametersSchemaBase = ...
    parameters_schema: dict = {}
    payload_schema: dict = {}


class TriggerTypeBaseDB(TriggerTypeBase):
    """Description of a specific kind/type of a trigger. The
       (pack, name) tuple is expected uniquely identify a trigger in
       the namespace of all triggers provided by a specific trigger_source.
    Attribute:
        name - Trigger type name.
        pack - Name of the content pack this trigger belongs to.
        trigger_source: Source that owns this trigger type.
        payload_info: Meta information of the expected payload.
    """

    id: int
    ref: str
    pack: str
    created_at: datetime = None
    updated_at: datetime = None


class TriggerDB(BaseModel):
    """
    Attribute:
        name - Trigger name.
        pack - Name of the content pack this trigger belongs to.
        type - Reference to the TriggerType object.
        parameters - Trigger parameters.
    """

    ref: str
    name: str = ...
    pack: str = ...
    type: str
    parameters: dict
    ref_count: int = 0
    # TODO: Calculate this uid based on info in this trigger
    uid: str


class TriggerInstanceDB(TriggerTypeBase):
    """An instance or occurrence of a type of Trigger.
    Attribute:
        trigger: Reference to the Trigger object.
        payload (dict): payload specific to the occurrence.
        occurrence_time (datetime): time of occurrence of the trigger.
    """

    trigger: str
    payload: dict
    occurrence_time: datetime = None
    status: str


# # smoke tests
# if "__main__" == __name__:
#     external_data = {}

#     trigger = TriggerTypeBaseDB(**external_data)
#     print(trigger)

#     print(trigger.name)
