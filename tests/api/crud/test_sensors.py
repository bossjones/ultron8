import pytest
from fastapi.encoders import jsonable_encoder

from tests.utils.utils import random_lower_string
from ultron8.api import crud
from ultron8.api.db.u_sqlite.session import db_session


from ultron8.api.models.sensors import SensorsBase
from ultron8.api.models.sensors import SensorsBaseInDB
from ultron8.api.models.sensors import SensorsCreate
from ultron8.api.models.sensors import SensorsUpdate
from ultron8.api.models.sensors import Sensor
from ultron8.api.models.sensors import SensorInDB

from ultron8.api.db_models.sensors import Sensors
from ultron8.api.db_models.sensors import SENSORS_TRIGGER_TYPES_ASSOCIATION
from ultron8.api.db_models.trigger import TriggerTypeDB
from ultron8.api.models.trigger import TriggerTypeInDBModel

from tests.utils.packs import create_random_packs
from tests.utils.trigger_instance import create_random_trigger_instance_name
from tests.utils.trigger_type import create_random_trigger_type
from tests.utils.trigger import create_random_trigger

from freezegun import freeze_time
from ultron8.debugger import debug_dump_exclude

from ultron8.api.models import orm_to_model

import json

from pydantic.json import pydantic_encoder


def pretty_lenient_json(data):
    return json.dumps(data, indent=2, default=pydantic_encoder) + "\n"


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.sensorsonly
@pytest.mark.unittest
def test_create_sensors():
    # Step 1 - create pack
    packs = create_random_packs()

    # FIXME: Something about this still doesn't work!
    # Step 2 - create trigger_type
    trigger_type1_orm = create_random_trigger_type(packs=packs)
    trigger_type2_orm = create_random_trigger_type(packs=packs)
    trigger_type3_orm = create_random_trigger_type(packs=packs)

    # trigger_type1_orm_data = jsonable_encoder(trigger_type1_orm)

    # import pdb;pdb.set_trace()

    trigger_type1 = TriggerTypeInDBModel.from_orm(trigger_type1_orm)
    trigger_type2 = TriggerTypeInDBModel.from_orm(trigger_type2_orm)
    trigger_type3 = TriggerTypeInDBModel.from_orm(trigger_type3_orm)

    # ValidationError: 4 validation errors
    # parameters_schema
    #   str type expected (type=type_error.str)
    # parameters_schema
    #   value is not none (type=type_error.none.allowed)
    # payload_schema
    #   str type expected (type=type_error.str)
    # payload_schema
    #   value is not none (type=type_error.none.allowed)

    # Step 3 - create trigger
    trigger1 = create_random_trigger(packs=packs, trigger_type=trigger_type1)
    trigger2 = create_random_trigger(packs=packs, trigger_type=trigger_type2)
    trigger3 = create_random_trigger(packs=packs, trigger_type=trigger_type3)

    trigger_type_list = crud.trigger_types.get_multi_by_packs_id(
        db_session, packs_id=packs.id, limit=3
    )

    # Step 4 - sensors arguments

    sensors_packs_name = packs.name
    sensors_class_name = "FileWatchSensor"
    sensors_enabled = True
    sensors_entry_point = "file_watch_sensor.py"
    sensors_description = "Sensor which monitors files for new lines"
    sensors_trigger_types = []
    # sensors_trigger_types.extend(trigger_type_list)
    # sensors_trigger_types.append(trigger1)
    # sensors_trigger_types.append(trigger2)
    # sensors_trigger_types.append(trigger3)
    #     {
    #         "name": "file_watch.line",
    #         "pack": "linux",
    #         "description": "Trigger which indicates a new line has been detected",
    #         "parameters_schema": {
    #             "type": "object",
    #             "properties": {
    #                 "file_path": {
    #                     "description": "Path to the file to monitor",
    #                     "type": "string",
    #                     "required": True,
    #                 }
    #             },
    #             "additionalProperties": False,
    #         },
    #         "payload_schema": {
    #             "type": "object",
    #             "properties": {
    #                 "file_path": {"type": "string"},
    #                 "file_name": {"type": "string"},
    #                 "line": {"type": "string"},
    #             },
    #         },
    #     }
    # ]

    # Step 5 - create sensors
    sensors_in = SensorsCreate(
        class_name=sensors_class_name,
        enabled=sensors_enabled,
        entry_point=sensors_entry_point,
        description=sensors_description,
        packs_name=sensors_packs_name,
        # trigger_types=sensors_trigger_types,
    )

    # import pdb;pdb.set_trace()
    sensors_in.trigger_types.append(trigger_type1)
    sensors_in.trigger_types.append(trigger_type2)
    sensors_in.trigger_types.append(trigger_type3)

    sensors = crud.sensors.create(db_session, sensors_in=sensors_in, packs_id=packs.id)

    sensors_get = crud.sensors.get(db_session=db_session, sensors_id=sensors.id)

    # Step 6 - validate sensors values in DB
    assert sensors_get.class_name == sensors_class_name
    assert sensors_get.enabled == sensors_enabled
    assert sensors_get.entry_point == sensors_entry_point
    assert sensors_get.description == sensors_description
    assert sensors_get.description == sensors_description
    assert sensors_get.packs_name == sensors_packs_name
    # sensors_trigger_types = sensors_get.trigger_types.filter(TriggerTypeDB.packs_id==packs.id)
    print("sensors_get.trigger_types: {}".format(sensors_get.trigger_types))
    print("sensors_get.trigger_types: {}".format(sensors_get.trigger_types))


# @freeze_time("2019-07-25 01:11:00.740428")
# @pytest.mark.sensorsonly
# @pytest.mark.unittest
# def test_get_sensors():
#     # Step 1 - create pack
#     packs = create_random_packs()

#     # Step 2 - create trigger_type
#     trigger_type = create_random_trigger_type(packs=packs)

#     # Step 3 - create trigger
#     trigger = create_random_trigger(packs=packs, trigger_type=trigger_type)

#     # Step 4 - sensors arguments
#     sensors_payload = {"foo": "bar", "name": "Joe"}
#     sensors_trigger = "{pack_name}.{trigger_name}".format(
#         pack_name=packs.name, trigger_name=trigger.name
#     )
#     sensors_status = "processed"

#     # Step 5 - create sensors
#     sensors_in = TriggerInstanceCreate(
#         trigger=sensors_trigger,
#         payload=sensors_payload,
#         status=sensors_status,
#     )
#     sensors = crud.sensors.create(
#         db_session, sensors_in=sensors_in
#     )

#     sensors_2 = crud.sensors.get(
#         db_session, sensors_id=sensors.id
#     )
#     assert jsonable_encoder(sensors) == jsonable_encoder(sensors_2)


# @freeze_time("2019-07-25 01:11:00.740428")
# @pytest.mark.sensorsonly
# @pytest.mark.unittest
# def test_get_by_trigger_sensors():
#     # Step 1 - create pack
#     packs = create_random_packs()

#     # Step 2 - create trigger_type
#     trigger_type = create_random_trigger_type(packs=packs)

#     # Step 3 - create trigger
#     trigger = create_random_trigger(packs=packs, trigger_type=trigger_type)

#     # Step 4 - sensors arguments
#     sensors_payload = {"foo": "bar", "name": "Joe"}
#     sensors_trigger = "{pack_name}.{trigger_name}".format(
#         pack_name=packs.name, trigger_name=trigger.name
#     )
#     sensors_status = "processed"

#     # Step 5 - create sensors
#     sensors_in = TriggerInstanceCreate(
#         trigger=sensors_trigger,
#         payload=sensors_payload,
#         status=sensors_status,
#     )
#     sensors = crud.sensors.create(
#         db_session, sensors_in=sensors_in
#     )

#     sensors_2 = crud.sensors.get_by_trigger(
#         db_session, sensors_trigger=sensors.trigger
#     )
#     assert jsonable_encoder(sensors) == jsonable_encoder(sensors_2)


# @freeze_time("2019-07-25 01:11:00.740428")
# @pytest.mark.sensorsonly
# @pytest.mark.unittest
# def test_get_multi_sensors():
#     # Step 1 - create pack
#     packs = create_random_packs()

#     # Step 2 - create trigger_type
#     trigger_type = create_random_trigger_type(packs=packs)

#     # Step 3 - create trigger
#     trigger = create_random_trigger(packs=packs, trigger_type=trigger_type)

#     # Step 4 - sensors arguments
#     sensors_payload0 = {"foo": "bar", "name": "Joe"}
#     sensors_trigger0 = "{pack_name}.{trigger_name}".format(
#         pack_name=packs.name, trigger_name=trigger.name
#     )
#     sensors_status0 = "processed"

#     # Step 5 - create sensors
#     sensors_in0 = TriggerInstanceCreate(
#         trigger=sensors_trigger0,
#         payload=sensors_payload0,
#         status=sensors_status0,
#     )
#     sensors0 = crud.sensors.create(
#         db_session, sensors_in=sensors_in0
#     )

#     # --------------------------------------------

#     # Step 4 - sensors arguments
#     sensors_payload1 = {"foo": "bar", "name": "Joe"}
#     sensors_trigger1 = "{pack_name}.{trigger_name}".format(
#         pack_name=packs.name, trigger_name=trigger.name
#     )
#     sensors_status1 = "processed"

#     # Step 5 - create sensors
#     sensors_in1 = TriggerInstanceCreate(
#         trigger=sensors_trigger1,
#         payload=sensors_payload1,
#         status=sensors_status1,
#     )
#     sensors1 = crud.sensors.create(
#         db_session, sensors_in=sensors_in1
#     )

#     sensors_2 = crud.sensors.get_multi(db_session)
#     for t in sensors_2:
#         assert type(t) == TriggerInstanceDB


# @freeze_time("2019-07-25 01:11:00.740428")
# @pytest.mark.sensorsonly
# @pytest.mark.unittest
# def test_update_sensors():
#     # Step 1 - create pack
#     packs = create_random_packs()

#     # Step 2 - create trigger_type
#     trigger_type = create_random_trigger_type(packs=packs)

#     # Step 3 - create trigger
#     trigger = create_random_trigger(packs=packs, trigger_type=trigger_type)

#     # Step 4 - sensors arguments
#     sensors_payload = {"foo": "bar", "name": "Joe"}
#     sensors_trigger = "{pack_name}.{trigger_name}".format(
#         pack_name=packs.name, trigger_name=trigger.name
#     )
#     sensors_status = "processed"

#     # Step 5 - create sensors
#     sensors_in = TriggerInstanceCreate(
#         trigger=sensors_trigger,
#         payload=sensors_payload,
#         status=sensors_status,
#     )
#     sensors = crud.sensors.create(
#         db_session, sensors_in=sensors_in
#     )
#     sensors_payload2 = {"foo": "bar1", "name": "Joe1"}

#     sensors_update = TriggerInstanceUpdate(payload=sensors_payload2)
#     sensors2 = crud.sensors.update(
#         db_session=db_session,
#         sensors=sensors,
#         sensors_in=sensors_update,
#     )

#     assert sensors2.trigger == sensors_trigger
#     assert sensors2.payload == sensors_payload2
#     assert sensors2.occurrence_time == "2019-07-25 01:11:00.740428"
#     assert sensors2.status == sensors_status


# @freeze_time("2019-07-25 01:11:00.740428")
# @pytest.mark.sensorsonly
# @pytest.mark.unittest
# def test_delete_sensors():
#     # Step 1 - create pack
#     packs = create_random_packs()

#     # Step 2 - create trigger_type
#     trigger_type = create_random_trigger_type(packs=packs)

#     # Step 3 - create trigger
#     trigger = create_random_trigger(packs=packs, trigger_type=trigger_type)

#     # Step 4 - sensors arguments
#     sensors_payload = {"foo": "bar", "name": "Joe"}
#     sensors_trigger = "{pack_name}.{trigger_name}".format(
#         pack_name=packs.name, trigger_name=trigger.name
#     )
#     sensors_status = "processed"

#     # Step 5 - create sensors
#     sensors_in = TriggerInstanceCreate(
#         trigger=sensors_trigger,
#         payload=sensors_payload,
#         status=sensors_status,
#     )
#     sensors = crud.sensors.create(
#         db_session, sensors_in=sensors_in
#     )

#     sensors2 = crud.sensors.remove(
#         db_session=db_session, sensors_id=sensors.id
#     )

#     sensors3 = crud.sensors.get(
#         db_session=db_session, sensors_id=sensors.id
#     )

#     assert sensors3 is None

#     assert sensors2.id == sensors.id
#     assert sensors2.trigger == sensors.trigger
#     assert sensors2.payload == sensors.payload
#     assert sensors2.occurrence_time == sensors.occurrence_time
