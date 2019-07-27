import requests

from tests.utils.utils import random_lower_string
from ultron8.api import crud
from ultron8.api.db.u_sqlite.session import db_session
from ultron8.api.models.trigger import TriggerTypeCreate
from tests.utils.user import create_random_user

import random
import string


def create_random_trigger_type_name():
    trigger_name_base = "ultron8"
    trigger_name_end = "".join(random.choices(string.ascii_lowercase, k=32))
    return "{}.{}".format(trigger_name_base, trigger_name_end)


def create_random_trigger_type(packs=None):
    trigger_type_name = create_random_trigger_type_name()
    trigger_type_packs_name = packs.name
    trigger_type_description = random_lower_string()
    trigger_type_parameters_schema = {
        "additionalProperties": False,
        "properties": {"url": {"type": "string", "required": True}},
        "type": "object",
    }

    trigger_type_payload_schema = {"type": "object"}

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

    trigger_type = crud.trigger_types.create(
        db_session, trigger_type_in=trigger_type_in, packs_id=packs.id
    )

    return trigger_type
