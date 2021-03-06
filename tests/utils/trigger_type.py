import random
import string

from typing import Optional

from fastapi.encoders import jsonable_encoder
import requests
from sqlalchemy.orm import Session
import ujson

from ultron8.api import crud
from ultron8.api.db_models.packs import Packs
from ultron8.api.db_models.trigger import TriggerTypeDB
from ultron8.api.models.trigger import TriggerTypeCreate

from tests.utils.user import create_random_user
from tests.utils.utils import random_lower_string


def create_random_trigger_type_name() -> str:
    trigger_name_base = "ultron8"
    trigger_name_end = "".join(random.choices(string.ascii_lowercase, k=32))
    return "{}.{}".format(trigger_name_base, trigger_name_end)


def build_random_trigger_type_create_model(
    packs: Optional[Packs] = None,
) -> TriggerTypeCreate:
    """Produces a pydantic model for TriggerTypeCreate

    Keyword Arguments:
        packs {Packs} -- Packs object (default: {None})

    Returns:
        [TriggerTypeCreate]
    """

    trigger_type_name = create_random_trigger_type_name()
    trigger_type_packs_name = packs.name
    trigger_type_description = random_lower_string()
    trigger_type_parameters_schema_dict = {
        "additionalProperties": False,
        "properties": {"url": {"type": "string", "required": True}},
        "type": "object",
    }
    trigger_type_payload_schema_dict = {"type": "object"}

    # FIXME: This needs to be fixed, are we turning it into a string or not 8/19/2019
    # trigger_type_parameters_schema = ujson.dumps(trigger_type_parameters_schema_dict)
    trigger_type_parameters_schema = trigger_type_parameters_schema_dict

    # FIXME: This needs to be fixed, are we turning it into a string or not 8/19/2019
    # trigger_type_payload_schema = ujson.dumps(trigger_type_payload_schema_dict)
    trigger_type_payload_schema = trigger_type_payload_schema_dict

    folder_name = trigger_type_name.split(".")

    trigger_type_metadata_file = "./tests/fixtures/simple/packs/{}".format(
        folder_name[1]
    )

    trigger_type_in = TriggerTypeCreate(
        name=trigger_type_name,
        packs_name=trigger_type_packs_name,
        description=trigger_type_description,
        payload_schema=trigger_type_payload_schema,
        parameters_schema=trigger_type_parameters_schema,
        metadata_file=trigger_type_metadata_file,
    )

    return trigger_type_in


def create_random_trigger_type(
    db: Session, packs: Optional[Packs] = None
) -> TriggerTypeDB:
    """Creates a pydantic TriggerTypeCreate then commits it to the database

    Keyword Arguments:
        packs {Packs} -- Packs object (default: {None})

    Returns:
        [TriggerTypeCreate]
    """
    trigger_type_in = build_random_trigger_type_create_model(packs=packs)

    trigger_type = crud.trigger_types.create(
        db, trigger_type_in=trigger_type_in, packs_id=packs.id
    )

    return trigger_type
