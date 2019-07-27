import pytest
from fastapi.encoders import jsonable_encoder

from tests.utils.utils import random_lower_string
from ultron8.api import crud
from ultron8.api.db.u_sqlite.session import db_session

from ultron8.api.models.trigger import TriggerTagsBase
from ultron8.api.models.trigger import TriggerTagsBaseInDB
from ultron8.api.models.trigger import TriggerTagsCreate
from ultron8.api.models.trigger import TriggerTagsUpdate
from ultron8.api.models.trigger import TriggerTypeBase
from ultron8.api.models.trigger import TriggerTypeBaseInDB
from ultron8.api.models.trigger import TriggerTypeCreate
from ultron8.api.models.trigger import TriggerTypeUpdate
from ultron8.api.models.trigger import TriggerBaseDB
from ultron8.api.models.trigger import TriggerBaseInDB
from ultron8.api.models.trigger import TriggerCreate
from ultron8.api.models.trigger import TriggerUpdate
from ultron8.api.models.trigger import TriggerInstanceBaseDB
from ultron8.api.models.trigger import TriggerInstanceBaseInDB
from ultron8.api.models.trigger import TriggerInstanceCreate
from ultron8.api.models.trigger import TriggerInstanceUpdate

from ultron8.api.models.packs import PacksCreate

from freezegun import freeze_time


TRIGGER_0 = {
    "name": "ultron8.test.trigger0",
    "pack": "dummy_pack_1",
    "description": "test trigger",
    "type": "dummy_pack_1.ultron8.test.triggertype0",
    "parameters": {},
}

TRIGGER_1 = {
    "name": "ultron8.test.trigger1",
    "pack": "dummy_pack_1",
    "description": "test trigger",
    "type": "dummy_pack_1.ultron8.test.triggertype1",
    "parameters": {},
}

TRIGGER_2 = {
    "name": "ultron8.test.trigger2",
    "pack": "dummy_pack_1",
    "description": "test trigger",
    "type": "dummy_pack_1.ultron8.test.triggertype2",
    "parameters": {"param1": {"foo": "bar"}},
}

TRIGGERTYPE_0 = {
    "name": "ultron8.test.triggertype0",
    "pack": "dummy_pack_1",
    "description": "test trigger",
    "payload_schema": {"tp1": None, "tp2": None, "tp3": None},
    "parameters_schema": {},
}
TRIGGERTYPE_1 = {
    "name": "ultron8.test.triggertype1",
    "pack": "dummy_pack_1",
    "description": "test trigger",
    "payload_schema": {"tp1": None, "tp2": None, "tp3": None},
}
TRIGGERTYPE_2 = {
    "name": "ultron8.test.triggertype2",
    "pack": "dummy_pack_1",
    "description": "test trigger",
    "payload_schema": {"tp1": None, "tp2": None, "tp3": None},
    "parameters_schema": {"param1": {"type": "object"}},
}


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.triggeronly
@pytest.mark.unittest
def test_create_trigger():
    packs_name = "dummy_pack_1"
    packs_description = random_lower_string()
    packs_keywords = random_lower_string()
    packs_version = random_lower_string()
    packs_python_versions = random_lower_string()
    packs_author = random_lower_string()
    packs_email = "info@theblacktonystark.com"
    packs_contributors = random_lower_string()
    packs_files = random_lower_string()
    packs_path = random_lower_string()
    packs_ref = "dummy_pack_1"

    trigger_name = TRIGGER_0["name"]
    trigger_packs_name = packs_name
    trigger_description = TRIGGER_0["description"]
    trigger_type = TRIGGER_0["type"]
    trigger_parameters = TRIGGER_0["parameters"]

    packs_in = PacksCreate(
        name=packs_name,
        description=packs_description,
        keywords=packs_keywords,
        version=packs_version,
        python_versions=packs_python_versions,
        author=packs_author,
        email=packs_email,
        contributors=packs_contributors,
        files=packs_files,
        path=packs_path,
        ref=packs_ref,
    )

    packs = crud.packs.create(db_session, packs_in=packs_in)

    trigger_in = TriggerCreate(
        name=trigger_name,
        packs_name=trigger_packs_name,
        description=trigger_description,
        type=trigger_type,
        parameters=trigger_parameters,
    )

    trigger = crud.trigger.create(db_session, trigger_in=trigger_in, packs_id=packs.id)

    assert trigger.name == trigger_name
    assert trigger.packs_name == trigger_packs_name
    assert trigger.description == trigger_description
    assert trigger.type == trigger_type
    assert trigger.parameters == trigger_parameters


# @freeze_time("2019-07-25 01:11:00.740428")
# @pytest.mark.triggeronly
# @pytest.mark.unittest
# def test_get_trigger():
#     packs_name = random_lower_string()
#     packs_description = random_lower_string()
#     packs_keywords = random_lower_string()
#     packs_version = random_lower_string()
#     packs_python_versions = random_lower_string()
#     packs_author = random_lower_string()
#     packs_email = "info@theblacktonystark.com"
#     packs_contributors = random_lower_string()
#     packs_files = random_lower_string()
#     packs_path = random_lower_string()
#     packs_ref = random_lower_string()

#     trigger_name = "check_loadavg"
#     trigger_runner_type = "remote-shell-script"
#     trigger_description = "Check CPU Load Average on a Host"
#     trigger_enabled = True
#     trigger_entry_point = "checks/check_loadavg.py"
#     trigger_parameters = {
#         "period": {
#             "enum": ["1", "5", "15", "all"],
#             "type": "string",
#             "description": "Time period for load avg: 1,5,15 minutes, or 'all'",
#             "default": "all",
#             "position": 0,
#         }
#     }

#     packs_in = PacksCreate(
#         name=packs_name,
#         description=packs_description,
#         keywords=packs_keywords,
#         version=packs_version,
#         python_versions=packs_python_versions,
#         author=packs_author,
#         email=packs_email,
#         contributors=packs_contributors,
#         files=packs_files,
#         path=packs_path,
#         ref=packs_ref,
#     )

#     packs = crud.packs.create(db_session, packs_in=packs_in)

#     trigger_in = TriggerCreate(
#         name=trigger_name,
#         runner_type=trigger_runner_type,
#         description=trigger_description,
#         enabled=trigger_enabled,
#         entry_point=trigger_entry_point,
#         parameters=trigger_parameters,
#         packs_name=packs_name,
#     )

#     trigger = crud.trigger.create(db_session, trigger_in=trigger_in, packs_id=packs.id)
#     trigger_2 = crud.trigger.get(db_session, trigger_id=trigger.id)
#     assert jsonable_encoder(trigger) == jsonable_encoder(trigger_2)


# @freeze_time("2019-07-25 01:11:00.740428")
# @pytest.mark.triggeronly
# @pytest.mark.unittest
# def test_update_trigger():
#     packs_name = random_lower_string()
#     packs_description = random_lower_string()
#     packs_keywords = random_lower_string()
#     packs_version = random_lower_string()
#     packs_python_versions = random_lower_string()
#     packs_author = random_lower_string()
#     packs_email = "info@theblacktonystark.com"
#     packs_contributors = random_lower_string()
#     packs_files = random_lower_string()
#     packs_path = random_lower_string()
#     packs_ref = random_lower_string()

#     trigger_name = "check_loadavg"
#     trigger_runner_type = "remote-shell-script"
#     trigger_description = "Check CPU Load Average on a Host"
#     trigger_enabled = True
#     trigger_entry_point = "checks/check_loadavg.py"
#     trigger_parameters = {
#         "period": {
#             "enum": ["1", "5", "15", "all"],
#             "type": "string",
#             "description": "Time period for load avg: 1,5,15 minutes, or 'all'",
#             "default": "all",
#             "position": 0,
#         }
#     }

#     packs_in = PacksCreate(
#         name=packs_name,
#         description=packs_description,
#         keywords=packs_keywords,
#         version=packs_version,
#         python_versions=packs_python_versions,
#         author=packs_author,
#         email=packs_email,
#         contributors=packs_contributors,
#         files=packs_files,
#         path=packs_path,
#         ref=packs_ref,
#     )

#     packs = crud.packs.create(db_session, packs_in=packs_in)

#     trigger_in = TriggerCreate(
#         name=trigger_name,
#         runner_type=trigger_runner_type,
#         description=trigger_description,
#         enabled=trigger_enabled,
#         entry_point=trigger_entry_point,
#         parameters=trigger_parameters,
#         packs_name=packs_name,
#     )

#     trigger = crud.trigger.create(db_session, trigger_in=trigger_in, packs_id=packs.id)
#     description2 = random_lower_string()
#     trigger_update = ActionUpdate(description=description2)
#     trigger2 = crud.trigger.update(
#         db_session=db_session, trigger=trigger, trigger_in=trigger_update
#     )

#     assert trigger.name == trigger2.name
#     assert trigger.runner_type == trigger2.runner_type
#     assert trigger.description == description2
#     assert trigger.enabled == trigger2.enabled
#     assert trigger.entry_point == trigger2.entry_point
#     assert trigger.parameters == trigger2.parameters
#     assert trigger.created_at == "2019-07-25 01:11:00.740428"
#     assert trigger.updated_at == "2019-07-25 01:11:00.740428"


# @freeze_time("2019-07-25 01:11:00.740428")
# @pytest.mark.triggeronly
# @pytest.mark.unittest
# def test_delete_trigger():
#     packs_name = random_lower_string()
#     packs_description = random_lower_string()
#     packs_keywords = random_lower_string()
#     packs_version = random_lower_string()
#     packs_python_versions = random_lower_string()
#     packs_author = random_lower_string()
#     packs_email = "info@theblacktonystark.com"
#     packs_contributors = random_lower_string()
#     packs_files = random_lower_string()
#     packs_path = random_lower_string()
#     packs_ref = random_lower_string()

#     trigger_name = "check_loadavg"
#     trigger_runner_type = "remote-shell-script"
#     trigger_description = "Check CPU Load Average on a Host"
#     trigger_enabled = True
#     trigger_entry_point = "checks/check_loadavg.py"
#     trigger_parameters = {
#         "period": {
#             "enum": ["1", "5", "15", "all"],
#             "type": "string",
#             "description": "Time period for load avg: 1,5,15 minutes, or 'all'",
#             "default": "all",
#             "position": 0,
#         }
#     }

#     packs_in = PacksCreate(
#         name=packs_name,
#         description=packs_description,
#         keywords=packs_keywords,
#         version=packs_version,
#         python_versions=packs_python_versions,
#         author=packs_author,
#         email=packs_email,
#         contributors=packs_contributors,
#         files=packs_files,
#         path=packs_path,
#         ref=packs_ref,
#     )

#     packs = crud.packs.create(db_session, packs_in=packs_in)

#     trigger_in = TriggerCreate(
#         name=trigger_name,
#         runner_type=trigger_runner_type,
#         description=trigger_description,
#         enabled=trigger_enabled,
#         entry_point=trigger_entry_point,
#         parameters=trigger_parameters,
#         packs_name=packs_name,
#     )

#     trigger = crud.trigger.create(db_session, trigger_in=trigger_in, packs_id=packs.id)

#     trigger2 = crud.trigger.remove(db_session=db_session, trigger_id=trigger.id)

#     trigger3 = crud.trigger.get(db_session=db_session, trigger_id=trigger.id)

#     assert trigger3 is None

#     assert trigger2.id == trigger.id
#     assert trigger2.name == trigger_name
#     assert trigger2.runner_type == trigger_runner_type
#     assert trigger2.description == trigger_description
#     assert trigger2.enabled == trigger_enabled
#     assert trigger2.entry_point == trigger_entry_point
#     assert trigger2.parameters == trigger_parameters
#     assert trigger2.created_at == "2019-07-25 01:11:00.740428"
#     assert trigger2.updated_at == "2019-07-25 01:11:00.740428"
