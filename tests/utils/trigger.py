import requests

from tests.utils.utils import random_lower_string
from ultron8.api import crud
from ultron8.api.db.u_sqlite.session import db_session
from ultron8.api.models.trigger import TriggerCreate
from tests.utils.user import create_random_user

import random
import string

from typing import Optional
from typing import Union
from ultron8.api.db_models.packs import Packs
from ultron8.api.db_models.trigger import TriggerDB, TriggerTypeDB
from ultron8.api.models.trigger import TriggerTypeInDBModel


def create_random_trigger_name():
    trigger_name_base = "ultron8"
    trigger_name_middle = "".join(random.choices(string.ascii_lowercase, k=32))
    trigger_name_end = "".join(random.choices(string.ascii_lowercase, k=32))
    return "{}.{}.{}".format(trigger_name_base, trigger_name_middle, trigger_name_end)


def create_trigger_type_from_name(pack_name="", trigger_name=""):
    random_num = random.randint(0, 9)
    return "{pack_name}.{trigger_name}{random_num}".format(
        pack_name=pack_name, trigger_name=trigger_name, random_num=random_num
    )


# def create_random_trigger(override_parameters={}):
#     """Create a random trigger db object

#     Returns:
#         [TriggerDB] -- TriggerDB object
#     """
#     # Create random pack
#     packs = create_random_user()

#     shared_name = create_random_trigger_name()
#     trigger_name = shared_name
#     trigger_packs_name = packs.name
#     trigger_description = random_lower_string()
#     trigger_type = create_trigger_type_from_name(
#         pack_name=packs.name, trigger_name=shared_name
#     )
#     trigger_parameters = override_parameters

#     trigger_in = TriggerCreate(
#         name=trigger_name,
#         packs_name=trigger_packs_name,
#         description=trigger_description,
#         type=trigger_type,
#         parameters=trigger_parameters,
#     )

#     trigger = crud.trigger.create(db_session, trigger_in=trigger_in, packs_id=packs.id)

#     return trigger


def create_random_trigger(
    packs: Optional[Packs] = None,
    trigger_type: Optional[Union[TriggerTypeDB, TriggerTypeInDBModel]] = None,
) -> TriggerDB:
    """Create a random trigger db object

    Returns:
        [TriggerDB] -- TriggerDB object
    """

    # shared_name = create_random_trigger_name()
    # trigger_name = shared_name.split(".")[1]
    shared_name = random_lower_string()
    trigger_name = shared_name
    trigger_packs_name = packs.name
    trigger_description = random_lower_string()

    trigger_type = "{pack_name}.{trigger_type_name}".format(
        pack_name=packs.name, trigger_type_name=trigger_type.name
    )

    trigger_parameters = {"url": "person"}

    trigger_in = TriggerCreate(
        name=trigger_name,
        packs_name=trigger_packs_name,
        description=trigger_description,
        type=trigger_type,
        parameters=trigger_parameters,
    )

    trigger = crud.trigger.create(db_session, trigger_in=trigger_in, packs_id=packs.id)

    return trigger
