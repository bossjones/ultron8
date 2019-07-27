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
from ultron8.api.db_models.trigger import TriggerTypeDB

from tests.utils.trigger_instance import create_random_trigger_instance_name
from tests.utils.packs import create_random_packs
from tests.utils.trigger_type import create_random_trigger_type
from tests.utils.trigger import create_random_trigger

from ultron8.api.models.packs import PacksCreate

from freezegun import freeze_time


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.triggerinstanceonly
@pytest.mark.unittest
def test_create_trigger_instance():
    # Step 1 - create pack
    packs = create_random_packs()

    # Step 2 - create trigger_type
    trigger_type = create_random_trigger_type(packs=packs)

    # Step 3 - create trigger
    trigger = create_random_trigger(packs=packs, trigger_type=trigger_type)

    # Step 4 - create trigger_instance

    trigger_instance_payload = {"foo": "bar", "name": "Joe"}

    trigger_instance_trigger = "{pack_name}.{trigger_name}".format(
        pack_name=packs.name, trigger_name=trigger.name
    )

    trigger_instance_status = "processed"

    trigger_instance_in = TriggerInstanceCreate(
        trigger=trigger_instance_trigger,
        payload=trigger_instance_payload,
        status=trigger_instance_status,
    )

    trigger_instance = crud.trigger_instance.create(
        db_session, trigger_instance_in=trigger_instance_in
    )

    assert trigger_instance.trigger == trigger_instance_trigger
    assert trigger_instance.payload == trigger_instance_payload
    assert trigger_instance.occurrence_time == "2019-07-25 01:11:00.740428"
    assert trigger_instance.status == trigger_instance_status


# @freeze_time("2019-07-25 01:11:00.740428")
# @pytest.mark.triggerinstanceonly
# @pytest.mark.unittest
# def test_get_trigger_instance():
#     packs = create_random_packs()

#     trigger_instance_name = create_random_trigger_instance_name()
#     trigger_instance_packs_name = packs.name
#     trigger_instance_description = random_lower_string()
#     trigger_instance_parameters_schema = {
#         "additionalProperties": False,
#         "properties": {"url": {"type": "string", "required": True}},
#         "type": "object",
#     }

#     trigger_instance_payload_schema = {"type": "object"}

#     folder_name = trigger_instance_name.split(".")

#     trigger_instance_metadata_file = "./tests/fixtures/simple/packs/{}".format(
#         folder_name[1]
#     )

#     trigger_instance_in = TriggerTypeCreate(
#         name=trigger_instance_name,
#         packs_name=trigger_instance_packs_name,
#         description=trigger_instance_description,
#         payload_schema=trigger_instance_payload_schema,
#         parameters_schema=trigger_instance_parameters_schema,
#         metadata_file=trigger_instance_metadata_file,
#     )

#     trigger_instance = crud.trigger_instances.create(
#         db_session, trigger_instance_in=trigger_instance_in, packs_id=packs.id
#     )

#     trigger_instance_2 = crud.trigger_instances.get(db_session, trigger_instance_id=trigger_instance.id)
#     assert jsonable_encoder(trigger_instance) == jsonable_encoder(trigger_instance_2)


# @freeze_time("2019-07-25 01:11:00.740428")
# @pytest.mark.triggerinstanceonly
# @pytest.mark.unittest
# def test_get_by_ref_trigger_instance():
#     packs = create_random_packs()

#     trigger_instance_name = create_random_trigger_instance_name()
#     trigger_instance_packs_name = packs.name
#     trigger_instance_description = random_lower_string()
#     trigger_instance_parameters_schema = {
#         "additionalProperties": False,
#         "properties": {"url": {"type": "string", "required": True}},
#         "type": "object",
#     }

#     trigger_instance_payload_schema = {"type": "object"}

#     folder_name = trigger_instance_name.split(".")

#     trigger_instance_metadata_file = "./tests/fixtures/simple/packs/{}".format(
#         folder_name[1]
#     )

#     trigger_instance_in = TriggerTypeCreate(
#         name=trigger_instance_name,
#         packs_name=trigger_instance_packs_name,
#         description=trigger_instance_description,
#         payload_schema=trigger_instance_payload_schema,
#         parameters_schema=trigger_instance_parameters_schema,
#         metadata_file=trigger_instance_metadata_file,
#     )

#     trigger_instance = crud.trigger_instances.create(
#         db_session, trigger_instance_in=trigger_instance_in, packs_id=packs.id
#     )

#     ref_lookup = "{}.{}".format(trigger_instance_packs_name, trigger_instance.name)
#     trigger_instance_2 = crud.trigger_instances.get_by_ref(db_session, ref=ref_lookup)
#     assert jsonable_encoder(trigger_instance) == jsonable_encoder(trigger_instance_2)


# @freeze_time("2019-07-25 01:11:00.740428")
# @pytest.mark.triggerinstanceonly
# @pytest.mark.unittest
# def test_get_by_name_trigger_instance():
#     packs = create_random_packs()

#     trigger_instance_name = create_random_trigger_instance_name()
#     trigger_instance_packs_name = packs.name
#     trigger_instance_description = random_lower_string()
#     trigger_instance_parameters_schema = {
#         "additionalProperties": False,
#         "properties": {"url": {"type": "string", "required": True}},
#         "type": "object",
#     }

#     trigger_instance_payload_schema = {"type": "object"}

#     folder_name = trigger_instance_name.split(".")

#     trigger_instance_metadata_file = "./tests/fixtures/simple/packs/{}".format(
#         folder_name[1]
#     )

#     trigger_instance_in = TriggerTypeCreate(
#         name=trigger_instance_name,
#         packs_name=trigger_instance_packs_name,
#         description=trigger_instance_description,
#         payload_schema=trigger_instance_payload_schema,
#         parameters_schema=trigger_instance_parameters_schema,
#         metadata_file=trigger_instance_metadata_file,
#     )

#     trigger_instance = crud.trigger_instances.create(
#         db_session, trigger_instance_in=trigger_instance_in, packs_id=packs.id
#     )
#     trigger_instance_2 = crud.trigger_instances.get_by_name(db_session, name=trigger_instance_name)
#     assert jsonable_encoder(trigger_instance) == jsonable_encoder(trigger_instance_2)


# @freeze_time("2019-07-25 01:11:00.740428")
# @pytest.mark.triggerinstanceonly
# @pytest.mark.unittest
# def test_get_multi_trigger_instance():
#     packs = create_random_packs()

#     trigger_instance_name0 = create_random_trigger_instance_name()
#     trigger_instance_packs_name0 = packs.name
#     trigger_instance_description0 = random_lower_string()
#     trigger_instance_parameters_schema0 = {
#         "additionalProperties": False,
#         "properties": {"url": {"type": "string", "required": True}},
#         "type": "object",
#     }

#     trigger_instance_payload_schema0 = {"type": "object"}

#     folder_name0 = trigger_instance_name0.split(".")

#     trigger_instance_metadata_file0 = "./tests/fixtures/simple/packs/{}".format(
#         folder_name0[1]
#     )

#     trigger_instance_in0 = TriggerTypeCreate(
#         name=trigger_instance_name0,
#         packs_name=trigger_instance_packs_name0,
#         description=trigger_instance_description0,
#         payload_schema=trigger_instance_payload_schema0,
#         parameters_schema=trigger_instance_parameters_schema0,
#         metadata_file=trigger_instance_metadata_file0,
#     )

#     trigger_instance0 = crud.trigger_instances.create(
#         db_session, trigger_instance_in=trigger_instance_in0, packs_id=packs.id
#     )

#     trigger_instance_name1 = create_random_trigger_instance_name()
#     trigger_instance_packs_name1 = packs.name
#     trigger_instance_description1 = random_lower_string()
#     trigger_instance_parameters_schema1 = {
#         "additionalProperties": False,
#         "properties": {"url": {"type": "string", "required": True}},
#         "type": "object",
#     }

#     trigger_instance_payload_schema1 = {"type": "object"}

#     folder_name1 = trigger_instance_name1.split(".")

#     trigger_instance_metadata_file1 = "./tests/fixtures/simple/packs/{}".format(
#         folder_name1[1]
#     )

#     trigger_instance_in1 = TriggerTypeCreate(
#         name=trigger_instance_name1,
#         packs_name=trigger_instance_packs_name1,
#         description=trigger_instance_description1,
#         payload_schema=trigger_instance_payload_schema1,
#         parameters_schema=trigger_instance_parameters_schema1,
#         metadata_file=trigger_instance_metadata_file1,
#     )

#     trigger_instance1 = crud.trigger_instances.create(
#         db_session, trigger_instance_in=trigger_instance_in1, packs_id=packs.id
#     )

#     trigger_instance_2 = crud.trigger_instances.get_multi(db_session)
#     for t in trigger_instance_2:
#         assert type(t) == TriggerTypeDB


# @freeze_time("2019-07-25 01:11:00.740428")
# @pytest.mark.triggerinstanceonly
# @pytest.mark.unittest
# def test_get_multi_by_packs_id_trigger_instance():
#     packs = create_random_packs()

#     trigger_instance_name0 = create_random_trigger_instance_name()
#     trigger_instance_packs_name0 = packs.name
#     trigger_instance_description0 = random_lower_string()
#     trigger_instance_parameters_schema0 = {
#         "additionalProperties": False,
#         "properties": {"url": {"type": "string", "required": True}},
#         "type": "object",
#     }

#     trigger_instance_payload_schema0 = {"type": "object"}

#     folder_name0 = trigger_instance_name0.split(".")

#     trigger_instance_metadata_file0 = "./tests/fixtures/simple/packs/{}".format(
#         folder_name0[1]
#     )

#     trigger_instance_in0 = TriggerTypeCreate(
#         name=trigger_instance_name0,
#         packs_name=trigger_instance_packs_name0,
#         description=trigger_instance_description0,
#         payload_schema=trigger_instance_payload_schema0,
#         parameters_schema=trigger_instance_parameters_schema0,
#         metadata_file=trigger_instance_metadata_file0,
#     )

#     trigger_instance0 = crud.trigger_instances.create(
#         db_session, trigger_instance_in=trigger_instance_in0, packs_id=packs.id
#     )

#     trigger_instance_name1 = create_random_trigger_instance_name()
#     trigger_instance_packs_name1 = packs.name
#     trigger_instance_description1 = random_lower_string()
#     trigger_instance_parameters_schema1 = {
#         "additionalProperties": False,
#         "properties": {"url": {"type": "string", "required": True}},
#         "type": "object",
#     }

#     trigger_instance_payload_schema1 = {"type": "object"}

#     folder_name1 = trigger_instance_name1.split(".")

#     trigger_instance_metadata_file1 = "./tests/fixtures/simple/packs/{}".format(
#         folder_name1[1]
#     )

#     trigger_instance_in1 = TriggerTypeCreate(
#         name=trigger_instance_name1,
#         packs_name=trigger_instance_packs_name1,
#         description=trigger_instance_description1,
#         payload_schema=trigger_instance_payload_schema1,
#         parameters_schema=trigger_instance_parameters_schema1,
#         metadata_file=trigger_instance_metadata_file1,
#     )

#     trigger_instance1 = crud.trigger_instances.create(
#         db_session, trigger_instance_in=trigger_instance_in1, packs_id=packs.id
#     )

#     trigger_instance_2 = crud.trigger_instances.get_multi_by_packs_id(
#         db_session, packs_id=packs.id, limit=2
#     )

#     for t in trigger_instance_2:
#         assert type(t) == TriggerTypeDB
#         assert t.packs_id == packs.id


# @freeze_time("2019-07-25 01:11:00.740428")
# @pytest.mark.triggerinstanceonly
# @pytest.mark.unittest
# def test_update_trigger_instance():
#     packs = create_random_packs()

#     trigger_instance_name = create_random_trigger_instance_name()
#     trigger_instance_packs_name = packs.name
#     trigger_instance_description = random_lower_string()
#     trigger_instance_parameters_schema = {
#         "additionalProperties": False,
#         "properties": {"url": {"type": "string", "required": True}},
#         "type": "object",
#     }

#     trigger_instance_payload_schema = {"type": "object"}

#     folder_name = trigger_instance_name.split(".")

#     trigger_instance_metadata_file = "./tests/fixtures/simple/packs/{}".format(
#         folder_name[1]
#     )

#     trigger_instance_in = TriggerTypeCreate(
#         name=trigger_instance_name,
#         packs_name=trigger_instance_packs_name,
#         description=trigger_instance_description,
#         payload_schema=trigger_instance_payload_schema,
#         parameters_schema=trigger_instance_parameters_schema,
#         metadata_file=trigger_instance_metadata_file,
#     )

#     trigger_instance = crud.trigger_instances.create(
#         db_session, trigger_instance_in=trigger_instance_in, packs_id=packs.id
#     )
#     description2 = random_lower_string()

#     trigger_instance_update = TriggerUpdate(description=description2)
#     trigger_instance2 = crud.trigger_instances.update(
#         db_session=db_session,
#         trigger_instance=trigger_instance,
#         trigger_instance_in=trigger_instance_update,
#     )

#     assert trigger_instance.name == trigger_instance2.name
#     assert trigger_instance.packs_name == trigger_instance2.packs_name
#     assert trigger_instance.description == description2
#     assert trigger_instance.parameters_schema == trigger_instance2.parameters_schema
#     assert trigger_instance.payload_schema == trigger_instance2.payload_schema


# @freeze_time("2019-07-25 01:11:00.740428")
# @pytest.mark.triggerinstanceonly
# @pytest.mark.unittest
# def test_delete_trigger_instance():
#     packs = create_random_packs()

#     trigger_instance_name = create_random_trigger_instance_name()
#     trigger_instance_packs_name = packs.name
#     trigger_instance_description = random_lower_string()
#     trigger_instance_parameters_schema = {
#         "additionalProperties": False,
#         "properties": {"url": {"type": "string", "required": True}},
#         "type": "object",
#     }

#     trigger_instance_payload_schema = {"type": "object"}

#     folder_name = trigger_instance_name.split(".")

#     trigger_instance_metadata_file = "./tests/fixtures/simple/packs/{}".format(
#         folder_name[1]
#     )

#     trigger_instance_in = TriggerTypeCreate(
#         name=trigger_instance_name,
#         packs_name=trigger_instance_packs_name,
#         description=trigger_instance_description,
#         payload_schema=trigger_instance_payload_schema,
#         parameters_schema=trigger_instance_parameters_schema,
#         metadata_file=trigger_instance_metadata_file,
#     )

#     trigger_instance = crud.trigger_instances.create(
#         db_session, trigger_instance_in=trigger_instance_in, packs_id=packs.id
#     )

#     trigger_instance2 = crud.trigger_instances.remove(
#         db_session=db_session, trigger_instance_id=trigger_instance.id
#     )

#     trigger_instance3 = crud.trigger_instances.get(
#         db_session=db_session, trigger_instance_id=trigger_instance.id
#     )

#     assert trigger_instance3 is None

#     assert trigger_instance2.id == trigger_instance.id
#     assert trigger_instance2.name == trigger_instance.name
#     assert trigger_instance2.packs_name == trigger_instance.packs_name
#     assert trigger_instance2.description == trigger_instance.description
#     assert trigger_instance2.parameters_schema == trigger_instance.parameters_schema
#     assert trigger_instance2.payload_schema == trigger_instance.payload_schema
