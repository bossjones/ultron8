from datetime import datetime
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import Union
from typing import Any

from pydantic import BaseModel
from pydantic import Schema

from pydantic import Json

######################################################################
# trigger_tags - START
######################################################################


class TriggerTagsBase(BaseModel):
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
    parameters_schema: Optional[Any] = None
    payload_schema: Optional[Any] = None


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

    id: int = None
    uid: str = None
    ref: Optional[str] = None
    name: str
    packs_name: str
    parameters_schema: Optional[Any] = None
    payload_schema: Optional[Any] = None
    metadata_file: Optional[str] = None


class TriggerTypeInDBModel(BaseModel):
    """ CONVERSION: Model used for converting SQLAlchemy Orm objects to pydantic Model. """

    id: int = None
    uid: str = None
    ref: Optional[str] = None
    name: str
    packs_name: str
    # SOURCE: https://github.com/tiangolo/fastapi/issues/211#issuecomment-491506412
    # @ebreton Pydantic's Json type expects a str containing valid JSON. Not a JSON-serializable-object.
    # If you know that the JSON value would be a dict, you could declare a dict there. If you knew it was a list you could declare that.
    # In this case, as we don't know the final value, and any valid JSON data would be accepted, you can use Any.
    # Here's a single file working example (just tested it with SQLite, that now also supports JSON columns):
    parameters_schema: Optional[Any] = None
    payload_schema: Optional[Any] = None
    metadata_file: Optional[str] = None

    class Config:
        orm_mode = True


class TriggerTypeCreate(TriggerTypeBaseInDB):
    id: int = None
    uid: str = None
    name: str
    packs_name: str
    parameters_schema: Optional[Any] = None
    payload_schema: Optional[Any] = None
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

# smoke-tests
# if "__main__" == __name__:

#     from ultron8.api.db_models.packs import Packs

#     pack_smoke_test = Packs(
#         name="smoke_test",
#         description="Generic Linux actions",
#         keywords="smoke_test",
#         version="0.1.0",
#         python_versions="3",
#         author="Jarvis",
#         email="info@theblacktonystark.com",
#         contributors="bossjones",
#         files="./tests/fixtures/simple/packs/smoke_test",
#         path="./tests/fixtures/simple/packs/smoke_test",
#         ref="linux",
#     )
#     print(pack_smoke_test)


#     # create_random_trigger_type(packs=pack_smoke_test)

#     trigger_type_name = create_random_trigger_type_name()
#     trigger_type_packs_name = packs.name
#     trigger_type_description = random_lower_string()
#     trigger_type_parameters_schema = {
#         "additionalProperties": False,
#         "properties": {"url": {"type": "string", "required": True}},
#         "type": "object",
#     }

#     trigger_type_payload_schema = {"type": "object"}

#     folder_name = trigger_type_name.split(".")

#     trigger_type_metadata_file = "./tests/fixtures/simple/packs/{}".format(
#         folder_name[1]
#     )

#     trigger_type_in = TriggerTypeCreate(
#         name=trigger_type_name,
#         packs_name=trigger_type_packs_name,
#         description=trigger_type_description,
#         payload_schema=trigger_type_payload_schema,
#         parameters_schema=trigger_type_parameters_schema,
#         metadata_file=trigger_type_metadata_file,
#     )

#     trigger_type = crud.trigger_types.create(
#         db_session, trigger_type_in=trigger_type_in, packs_id=packs.id
#     )
