from fastapi.encoders import jsonable_encoder
from freezegun import freeze_time
import pytest
from sqlalchemy.orm import Session

from ultron8.api import crud
from ultron8.api.db_models.trigger import TriggerInstanceDB
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
from tests.utils.trigger import create_random_trigger
from tests.utils.trigger_instance import create_random_trigger_instance_name
from tests.utils.trigger_type import create_random_trigger_type
from tests.utils.utils import random_lower_string


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.triggerinstanceonly
@pytest.mark.unittest
def test_create_trigger_instance(db: Session) -> None:
    # Step 1 - create pack
    packs = create_random_packs(db)

    # Step 2 - create trigger_type
    trigger_type = create_random_trigger_type(db, packs=packs)

    # Step 3 - create trigger
    trigger = create_random_trigger(db, packs=packs, trigger_type=trigger_type)

    # Step 4 - trigger_instance arguments
    trigger_instance_payload = {"foo": "bar", "name": "Joe"}
    trigger_instance_trigger = "{pack_name}.{trigger_name}".format(
        pack_name=packs.name, trigger_name=trigger.name
    )
    trigger_instance_status = "processed"

    # Step 5 - create trigger_instance
    trigger_instance_in = TriggerInstanceCreate(
        trigger=trigger_instance_trigger,
        payload=trigger_instance_payload,
        status=trigger_instance_status,
    )
    trigger_instance = crud.trigger_instance.create(
        db, trigger_instance_in=trigger_instance_in
    )

    # Step 6 - validate trigger_instance values in DB
    assert trigger_instance.trigger == trigger_instance_trigger
    assert trigger_instance.payload == trigger_instance_payload
    assert trigger_instance.occurrence_time == "2019-07-25 01:11:00.740428"
    assert trigger_instance.status == trigger_instance_status


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.triggerinstanceonly
@pytest.mark.unittest
def test_get_trigger_instance(db: Session) -> None:
    # Step 1 - create pack
    packs = create_random_packs(db)

    # Step 2 - create trigger_type
    trigger_type = create_random_trigger_type(db, packs=packs)

    # Step 3 - create trigger
    trigger = create_random_trigger(db, packs=packs, trigger_type=trigger_type)

    # Step 4 - trigger_instance arguments
    trigger_instance_payload = {"foo": "bar", "name": "Joe"}
    trigger_instance_trigger = "{pack_name}.{trigger_name}".format(
        pack_name=packs.name, trigger_name=trigger.name
    )
    trigger_instance_status = "processed"

    # Step 5 - create trigger_instance
    trigger_instance_in = TriggerInstanceCreate(
        trigger=trigger_instance_trigger,
        payload=trigger_instance_payload,
        status=trigger_instance_status,
    )
    trigger_instance = crud.trigger_instance.create(
        db, trigger_instance_in=trigger_instance_in
    )

    trigger_instance_2 = crud.trigger_instance.get(
        db, trigger_instance_id=trigger_instance.id
    )
    assert jsonable_encoder(trigger_instance) == jsonable_encoder(trigger_instance_2)


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.triggerinstanceonly
@pytest.mark.unittest
def test_get_by_trigger_trigger_instance(db: Session) -> None:
    # Step 1 - create pack
    packs = create_random_packs(db)

    # Step 2 - create trigger_type
    trigger_type = create_random_trigger_type(db, packs=packs)

    # Step 3 - create trigger
    trigger = create_random_trigger(db, packs=packs, trigger_type=trigger_type)

    # Step 4 - trigger_instance arguments
    trigger_instance_payload = {"foo": "bar", "name": "Joe"}
    trigger_instance_trigger = "{pack_name}.{trigger_name}".format(
        pack_name=packs.name, trigger_name=trigger.name
    )
    trigger_instance_status = "processed"

    # Step 5 - create trigger_instance
    trigger_instance_in = TriggerInstanceCreate(
        trigger=trigger_instance_trigger,
        payload=trigger_instance_payload,
        status=trigger_instance_status,
    )
    trigger_instance = crud.trigger_instance.create(
        db, trigger_instance_in=trigger_instance_in
    )

    trigger_instance_2 = crud.trigger_instance.get_by_trigger(
        db, trigger_instance_trigger=trigger_instance.trigger
    )
    assert jsonable_encoder(trigger_instance) == jsonable_encoder(trigger_instance_2)


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.triggerinstanceonly
@pytest.mark.unittest
def test_get_multi_trigger_instance(db: Session) -> None:
    # Step 1 - create pack
    packs = create_random_packs(db)

    # Step 2 - create trigger_type
    trigger_type = create_random_trigger_type(db, packs=packs)

    # Step 3 - create trigger
    trigger = create_random_trigger(db, packs=packs, trigger_type=trigger_type)

    # Step 4 - trigger_instance arguments
    trigger_instance_payload0 = {"foo": "bar", "name": "Joe"}
    trigger_instance_trigger0 = "{pack_name}.{trigger_name}".format(
        pack_name=packs.name, trigger_name=trigger.name
    )
    trigger_instance_status0 = "processed"

    # Step 5 - create trigger_instance
    trigger_instance_in0 = TriggerInstanceCreate(
        trigger=trigger_instance_trigger0,
        payload=trigger_instance_payload0,
        status=trigger_instance_status0,
    )
    trigger_instance0 = crud.trigger_instance.create(
        db, trigger_instance_in=trigger_instance_in0
    )

    # --------------------------------------------

    # Step 4 - trigger_instance arguments
    trigger_instance_payload1 = {"foo": "bar", "name": "Joe"}
    trigger_instance_trigger1 = "{pack_name}.{trigger_name}".format(
        pack_name=packs.name, trigger_name=trigger.name
    )
    trigger_instance_status1 = "processed"

    # Step 5 - create trigger_instance
    trigger_instance_in1 = TriggerInstanceCreate(
        trigger=trigger_instance_trigger1,
        payload=trigger_instance_payload1,
        status=trigger_instance_status1,
    )
    trigger_instance1 = crud.trigger_instance.create(
        db, trigger_instance_in=trigger_instance_in1
    )

    trigger_instance_2 = crud.trigger_instance.get_multi(db)
    for t in trigger_instance_2:
        assert type(t) == TriggerInstanceDB


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.triggerinstanceonly
@pytest.mark.unittest
def test_update_trigger_instance(db: Session) -> None:
    # Step 1 - create pack
    packs = create_random_packs(db)

    # Step 2 - create trigger_type
    trigger_type = create_random_trigger_type(db, packs=packs)

    # Step 3 - create trigger
    trigger = create_random_trigger(db, packs=packs, trigger_type=trigger_type)

    # Step 4 - trigger_instance arguments
    trigger_instance_payload = {"foo": "bar", "name": "Joe"}
    trigger_instance_trigger = "{pack_name}.{trigger_name}".format(
        pack_name=packs.name, trigger_name=trigger.name
    )
    trigger_instance_status = "processed"

    # Step 5 - create trigger_instance
    trigger_instance_in = TriggerInstanceCreate(
        trigger=trigger_instance_trigger,
        payload=trigger_instance_payload,
        status=trigger_instance_status,
    )
    trigger_instance = crud.trigger_instance.create(
        db, trigger_instance_in=trigger_instance_in
    )
    trigger_instance_payload2 = {"foo": "bar1", "name": "Joe1"}

    trigger_instance_update = TriggerInstanceUpdate(payload=trigger_instance_payload2)
    trigger_instance2 = crud.trigger_instance.update(
        db_session=db,
        trigger_instance=trigger_instance,
        trigger_instance_in=trigger_instance_update,
    )

    assert trigger_instance2.trigger == trigger_instance_trigger
    assert trigger_instance2.payload == trigger_instance_payload2
    assert trigger_instance2.occurrence_time == "2019-07-25 01:11:00.740428"
    assert trigger_instance2.status == trigger_instance_status


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.triggerinstanceonly
@pytest.mark.unittest
def test_delete_trigger_instance(db: Session) -> None:
    # Step 1 - create pack
    packs = create_random_packs(db)

    # Step 2 - create trigger_type
    trigger_type = create_random_trigger_type(db, packs=packs)

    # Step 3 - create trigger
    trigger = create_random_trigger(db, packs=packs, trigger_type=trigger_type)

    # Step 4 - trigger_instance arguments
    trigger_instance_payload = {"foo": "bar", "name": "Joe"}
    trigger_instance_trigger = "{pack_name}.{trigger_name}".format(
        pack_name=packs.name, trigger_name=trigger.name
    )
    trigger_instance_status = "processed"

    # Step 5 - create trigger_instance
    trigger_instance_in = TriggerInstanceCreate(
        trigger=trigger_instance_trigger,
        payload=trigger_instance_payload,
        status=trigger_instance_status,
    )
    trigger_instance = crud.trigger_instance.create(
        db, trigger_instance_in=trigger_instance_in
    )

    trigger_instance2 = crud.trigger_instance.remove(
        db_session=db, trigger_instance_id=trigger_instance.id
    )

    trigger_instance3 = crud.trigger_instance.get(
        db_session=db, trigger_instance_id=trigger_instance.id
    )

    assert trigger_instance3 is None

    assert trigger_instance2.id == trigger_instance.id
    assert trigger_instance2.trigger == trigger_instance.trigger
    assert trigger_instance2.payload == trigger_instance.payload
    assert trigger_instance2.occurrence_time == trigger_instance.occurrence_time
