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

######################################################################
# trigger_tags - START
######################################################################


class TriggerTagsBase(BaseModel):
    id: Optional[int] = None
    trigger_type_id: Optional[int] = None
    tag: Optional[str] = None
    trigger_name: Optional[str] = None


class TriggerTagsBaseInDB(TriggerTagsBase):
    id: int = None
    trigger_type_id: int
    tag: str
    trigger_name: str


class TriggerTagsCreate(TriggerTagsBaseInDB):
    trigger_type_id: int = None
    tag: str = None
    trigger_name: str = None


class TriggerTagsUpdate(TriggerTagsBaseInDB):
    pass


######################################################################
# trigger_tags - END
######################################################################

######################################################################
# trigger_types - START
######################################################################
class TriggerTypeBase(BaseModel):
    uid: Optional[str] = None
    name: Optional[str] = None
    ref: Optional[str] = None
    packs_name: Optional[str] = None
    description: Optional[str] = None
    parameters_schema: Optional[dict] = {}
    payload_schema: Optional[dict] = {}


class TriggerTypeBaseInDB(TriggerTypeBase):
    """Description of a specific kind/type of a trigger. The
       (pack, name) tuple is expected uniquely identify a trigger in
       the namespace of all triggers provided by a specific trigger_source.
    Attribute:
        name - Trigger type name.
        packs_name - Name of the content pack this trigger belongs to.
        trigger_source: Source that owns this trigger type.
        payload_info: Meta information of the expected payload.
    """

    id: Optional[int] = None
    uid: str = None
    ref: Optional[str] = None
    name: str
    packs_name: str
    parameters_schema: Optional[dict] = {}
    payload_schema: Optional[dict] = {}
    metadata_file: Optional[str] = None


class TriggerTypeCreate(TriggerTypeBaseInDB):
    id: int = None
    uid: str = None
    name: str
    packs_name: str
    parameters_schema: Optional[dict] = {}
    payload_schema: Optional[dict] = {}
    metadata_file: Optional[str] = None


class TriggerTypeUpdate(TriggerTypeBaseInDB):
    pass


######################################################################
# trigger_types - END
######################################################################

######################################################################
# triggers - START
######################################################################


class TriggerBaseDB(BaseModel):
    """
    Attribute:
        name - Trigger name.
        pack - Name of the content pack this trigger belongs to.
        type - Reference to the TriggerType object.
        parameters - Trigger parameters.
    """

    ref: Optional[str] = None
    name: Optional[str] = None
    uid: Optional[str] = None
    description: Optional[str] = None
    packs_name: Optional[str] = None
    type: Optional[str] = None
    parameters: Optional[dict] = {}
    ref_count: Optional[int] = 0


class TriggerBaseInDB(TriggerBaseDB):
    """
    Attribute:
        name - Trigger name.
        pack - Name of the content pack this trigger belongs to.
        type - Reference to the TriggerType object.
        parameters - Trigger parameters.
    """

    id: int = None
    uid: str = None


class TriggerCreate(TriggerBaseInDB):
    ref: Optional[str] = None
    name: str


class TriggerUpdate(TriggerBaseInDB):
    pass


######################################################################
# triggers - END
######################################################################


######################################################################
# trigger_events - START
######################################################################
class TriggerInstanceBaseDB(BaseModel):
    """An instance or occurrence of a type of Trigger.
    Attribute:
        trigger: Reference to the Trigger object.
        payload (dict): payload specific to the occurrence.
        occurrence_time (datetime): time of occurrence of the trigger.
    """

    trigger: Optional[str] = None
    payload: Optional[dict] = {}
    occurrence_time: datetime = None
    status: Optional[str] = None


class TriggerInstanceBaseInDB(TriggerInstanceBaseDB):
    id: int = None


class TriggerInstanceCreate(TriggerInstanceBaseInDB):
    trigger: str = None
    payload: dict = {}
    status: str = None


class TriggerInstanceUpdate(TriggerInstanceBaseInDB):
    pass


######################################################################
# trigger_events - END
######################################################################
