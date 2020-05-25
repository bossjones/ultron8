from fastapi.encoders import jsonable_encoder
from freezegun import freeze_time
import pytest
from sqlalchemy.orm import Session
import ujson

from ultron8.api import crud
from ultron8.api.db_models.trigger import TriggerTypeDB
from ultron8.api.models.packs import PacksCreate
from ultron8.api.models.trigger import (
    TriggerBaseDB,
    TriggerBaseInDB,
    TriggerCreate,
    TriggerInstanceBaseDB,
    TriggerInstanceBaseInDB,
    TriggerInstanceCreate,
    TriggerInstanceUpdate,
    TriggerTagsBase,
    TriggerTagsBaseInDB,
    TriggerTagsCreate,
    TriggerTagsUpdate,
    TriggerTypeBase,
    TriggerTypeBaseInDB,
    TriggerTypeCreate,
    TriggerTypeUpdate,
    TriggerUpdate,
)

from tests.utils.packs import create_random_packs
from tests.utils.trigger_type import create_random_trigger_type_name
from tests.utils.utils import random_lower_string


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.triggertypeonly
@pytest.mark.unittest
def test_create_trigger_type(db: Session) -> None:
    packs = create_random_packs(db)

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
        db, trigger_type_in=trigger_type_in, packs_id=packs.id
    )

    assert trigger_type.name == trigger_type_name
    assert trigger_type.packs_name == trigger_type_packs_name
    assert trigger_type.description == trigger_type_description
    assert trigger_type.parameters_schema == trigger_type_parameters_schema
    assert trigger_type.payload_schema == trigger_type_payload_schema


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.triggertypeonly
@pytest.mark.unittest
def test_get_trigger_type(db: Session) -> None:
    packs = create_random_packs(db)

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
        db, trigger_type_in=trigger_type_in, packs_id=packs.id
    )

    trigger_type_2 = crud.trigger_types.get(db, trigger_type_id=trigger_type.id)
    assert jsonable_encoder(trigger_type) == jsonable_encoder(trigger_type_2)


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.triggertypeonly
@pytest.mark.unittest
def test_get_by_ref_trigger_type(db: Session) -> None:
    packs = create_random_packs(db)

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
        db, trigger_type_in=trigger_type_in, packs_id=packs.id
    )

    ref_lookup = "{}.{}".format(trigger_type_packs_name, trigger_type.name)
    trigger_type_2 = crud.trigger_types.get_by_ref(db, ref=ref_lookup)
    assert jsonable_encoder(trigger_type) == jsonable_encoder(trigger_type_2)


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.triggertypeonly
@pytest.mark.unittest
def test_get_by_name_trigger_type(db: Session) -> None:
    packs = create_random_packs(db)

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
        db, trigger_type_in=trigger_type_in, packs_id=packs.id
    )
    trigger_type_2 = crud.trigger_types.get_by_name(db, name=trigger_type_name)
    assert jsonable_encoder(trigger_type) == jsonable_encoder(trigger_type_2)


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.triggertypeonly
@pytest.mark.unittest
def test_get_multi_trigger_type(db: Session) -> None:
    packs = create_random_packs(db)

    trigger_type_name0 = create_random_trigger_type_name()
    trigger_type_packs_name0 = packs.name
    trigger_type_description0 = random_lower_string()
    trigger_type_parameters_schema0 = {
        "additionalProperties": False,
        "properties": {"url": {"type": "string", "required": True}},
        "type": "object",
    }

    trigger_type_payload_schema0 = {"type": "object"}

    folder_name0 = trigger_type_name0.split(".")

    trigger_type_metadata_file0 = "./tests/fixtures/simple/packs/{}".format(
        folder_name0[1]
    )

    trigger_type_in0 = TriggerTypeCreate(
        name=trigger_type_name0,
        packs_name=trigger_type_packs_name0,
        description=trigger_type_description0,
        payload_schema=trigger_type_payload_schema0,
        parameters_schema=trigger_type_parameters_schema0,
        metadata_file=trigger_type_metadata_file0,
    )

    trigger_type0 = crud.trigger_types.create(
        db, trigger_type_in=trigger_type_in0, packs_id=packs.id
    )

    trigger_type_name1 = create_random_trigger_type_name()
    trigger_type_packs_name1 = packs.name
    trigger_type_description1 = random_lower_string()
    trigger_type_parameters_schema1 = {
        "additionalProperties": False,
        "properties": {"url": {"type": "string", "required": True}},
        "type": "object",
    }

    trigger_type_payload_schema1 = {"type": "object"}

    folder_name1 = trigger_type_name1.split(".")

    trigger_type_metadata_file1 = "./tests/fixtures/simple/packs/{}".format(
        folder_name1[1]
    )

    trigger_type_in1 = TriggerTypeCreate(
        name=trigger_type_name1,
        packs_name=trigger_type_packs_name1,
        description=trigger_type_description1,
        payload_schema=trigger_type_payload_schema1,
        parameters_schema=trigger_type_parameters_schema1,
        metadata_file=trigger_type_metadata_file1,
    )

    trigger_type1 = crud.trigger_types.create(
        db, trigger_type_in=trigger_type_in1, packs_id=packs.id
    )

    trigger_type_2 = crud.trigger_types.get_multi(db)
    for t in trigger_type_2:
        assert type(t) == TriggerTypeDB


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.triggertypeonly
@pytest.mark.unittest
def test_get_multi_by_packs_id_trigger_type(db: Session) -> None:
    packs = create_random_packs(db)

    trigger_type_name0 = create_random_trigger_type_name()
    trigger_type_packs_name0 = packs.name
    trigger_type_description0 = random_lower_string()
    trigger_type_parameters_schema0 = {
        "additionalProperties": False,
        "properties": {"url": {"type": "string", "required": True}},
        "type": "object",
    }

    trigger_type_payload_schema0 = {"type": "object"}

    folder_name0 = trigger_type_name0.split(".")

    trigger_type_metadata_file0 = "./tests/fixtures/simple/packs/{}".format(
        folder_name0[1]
    )

    trigger_type_in0 = TriggerTypeCreate(
        name=trigger_type_name0,
        packs_name=trigger_type_packs_name0,
        description=trigger_type_description0,
        payload_schema=trigger_type_payload_schema0,
        parameters_schema=trigger_type_parameters_schema0,
        metadata_file=trigger_type_metadata_file0,
    )

    trigger_type0 = crud.trigger_types.create(
        db, trigger_type_in=trigger_type_in0, packs_id=packs.id
    )

    trigger_type_name1 = create_random_trigger_type_name()
    trigger_type_packs_name1 = packs.name
    trigger_type_description1 = random_lower_string()
    trigger_type_parameters_schema1 = {
        "additionalProperties": False,
        "properties": {"url": {"type": "string", "required": True}},
        "type": "object",
    }

    trigger_type_payload_schema1 = {"type": "object"}

    folder_name1 = trigger_type_name1.split(".")

    trigger_type_metadata_file1 = "./tests/fixtures/simple/packs/{}".format(
        folder_name1[1]
    )

    trigger_type_in1 = TriggerTypeCreate(
        name=trigger_type_name1,
        packs_name=trigger_type_packs_name1,
        description=trigger_type_description1,
        payload_schema=trigger_type_payload_schema1,
        parameters_schema=trigger_type_parameters_schema1,
        metadata_file=trigger_type_metadata_file1,
    )

    trigger_type1 = crud.trigger_types.create(
        db, trigger_type_in=trigger_type_in1, packs_id=packs.id
    )

    trigger_type_2 = crud.trigger_types.get_multi_by_packs_id(
        db, packs_id=packs.id, limit=2
    )

    for t in trigger_type_2:
        assert type(t) == TriggerTypeDB
        assert t.packs_id == packs.id


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.triggertypeonly
@pytest.mark.unittest
def test_update_trigger_type(db: Session) -> None:
    packs = create_random_packs(db)

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
        db, trigger_type_in=trigger_type_in, packs_id=packs.id
    )
    description2 = random_lower_string()

    trigger_type_update = TriggerUpdate(description=description2)
    trigger_type2 = crud.trigger_types.update(
        db_session=db, trigger_type=trigger_type, trigger_type_in=trigger_type_update,
    )

    assert trigger_type.name == trigger_type2.name
    assert trigger_type.packs_name == trigger_type2.packs_name
    assert trigger_type.description == description2
    assert trigger_type.parameters_schema == trigger_type2.parameters_schema
    assert trigger_type.payload_schema == trigger_type2.payload_schema


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.triggertypeonly
@pytest.mark.unittest
def test_delete_trigger_type(db: Session) -> None:
    packs = create_random_packs(db)

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
    trigger_type_parameters_schema = ujson.dumps(trigger_type_parameters_schema_dict)
    # trigger_type_parameters_schema = trigger_type_parameters_schema_dict

    # FIXME: This needs to be fixed, are we turning it into a string or not 8/19/2019
    trigger_type_payload_schema = ujson.dumps(trigger_type_payload_schema_dict)
    # trigger_type_payload_schema = trigger_type_payload_schema_dict

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
        db, trigger_type_in=trigger_type_in, packs_id=packs.id
    )

    trigger_type2 = crud.trigger_types.remove(
        db_session=db, trigger_type_id=trigger_type.id
    )

    trigger_type3 = crud.trigger_types.get(
        db_session=db, trigger_type_id=trigger_type.id
    )

    assert trigger_type3 is None

    assert trigger_type2.id == trigger_type.id
    assert trigger_type2.name == trigger_type.name
    assert trigger_type2.packs_name == trigger_type.packs_name
    assert trigger_type2.description == trigger_type.description
    assert trigger_type2.parameters_schema == trigger_type.parameters_schema
    assert trigger_type2.payload_schema == trigger_type.payload_schema
