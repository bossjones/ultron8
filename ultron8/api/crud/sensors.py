import os
from typing import List
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ultron8.api.core.security import get_password_hash
from ultron8.api.core.security import verify_password
from ultron8.api.db_models.sensors import Sensors
from ultron8.api.models.sensors import SensorsCreate
from ultron8.api.models.sensors import SensorsUpdate

from ultron8.constants.packs import SYSTEM_PACK_NAME
from ultron8.constants.sensors import MINIMUM_POLL_INTERVAL


def get(db_session: Session, *, sensors_id: int) -> Optional[Sensors]:
    return db_session.query(Sensors).filter(Sensors.id == sensors_id).first()


def get_by_ref(db_session: Session, *, ref: str) -> Optional[Sensors]:
    return db_session.query(Sensors).filter(Sensors.ref == ref).first()


def get_multi(db_session: Session, *, skip=0, limit=100) -> List[Optional[Sensors]]:
    return db_session.query(Sensors).offset(skip).limit(limit).all()


def get_multi_by_packs_id(
    db_session: Session, *, packs_id: int, skip=0, limit=100
) -> List[Optional[Sensors]]:
    return (
        db_session.query(Sensors)
        .filter(Sensors.packs_id == packs_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


# # TODO: Enable these
# def to_sensor_db_model(sensor_api_model=None):
#     """
#     Converts a SensorTypeAPI model to DB model.
#     Also, creates trigger type objects provided in SensorTypeAPI.
#     :param sensor_api_model: SensorTypeAPI object.
#     :type sensor_api_model: :class:`SensorTypeAPI`
#     :rtype: :class:`SensorTypeDB`
#     """
#     class_name = getattr(sensor_api_model, 'class_name', None)
#     packs_name = getattr(sensor_api_model, 'packs_name', None)
#     entry_point = get_sensor_entry_point(sensor_api_model)
#     artifact_uri = getattr(sensor_api_model, 'artifact_uri', None)
#     description = getattr(sensor_api_model, 'description', None)
#     trigger_types = getattr(sensor_api_model, 'trigger_types', [])
#     poll_interval = getattr(sensor_api_model, 'poll_interval', None)
#     enabled = getattr(sensor_api_model, 'enabled', True)
#     metadata_file = getattr(sensor_api_model, 'metadata_file', None)

#     poll_interval = getattr(sensor_api_model, 'poll_interval', None)
#     if poll_interval and (poll_interval < MINIMUM_POLL_INTERVAL):
#         raise ValueError('Minimum possible poll_interval is %s seconds' %
#                          (MINIMUM_POLL_INTERVAL))

#     # Add pack and metadata fileto each trigger type item
#     for trigger_type in trigger_types:
#         trigger_type['packs_name'] = packs_name
#         trigger_type['metadata_file'] = metadata_file

#     trigger_type_refs = create_trigger_types(trigger_types)

#     return _create_sensor_type(pack=pack,
#                                name=class_name,
#                                description=description,
#                                artifact_uri=artifact_uri,
#                                entry_point=entry_point,
#                                trigger_types=trigger_type_refs,
#                                poll_interval=poll_interval,
#                                enabled=enabled,
#                                metadata_file=metadata_file)


# def create_trigger_types(trigger_types, metadata_file=None):
#     if not trigger_types:
#         return []

#     # Add TrigerType models to the DB
#     trigger_type_dbs = trigger_service.add_trigger_models(trigger_types=trigger_types)

#     trigger_type_refs = []
#     # Populate a list of references belonging to this sensor
#     for trigger_type_db, _ in trigger_type_dbs:
#         ref_obj = trigger_type_db.get_reference()
#         trigger_type_ref = ref_obj.ref
#         trigger_type_refs.append(trigger_type_ref)
#     return trigger_type_refs


# def _create_sensor_type(pack=None, name=None, description=None, artifact_uri=None,
#                         entry_point=None, trigger_types=None, poll_interval=10,
#                         enabled=True, metadata_file=None):

#     sensor_type = SensorTypeDB(pack=pack, name=name, description=description,
#                                artifact_uri=artifact_uri, entry_point=entry_point,
#                                poll_interval=poll_interval, enabled=enabled,
#                                trigger_types=trigger_types, metadata_file=metadata_file)
#     return sensor_type

# def create(db_session: Session, *, sensors_in: SensorsCreate, packs_id: int) -> Sensors:
#     import pdb;pdb.set_trace()
#     trigger_type_data = []
#     sensors_in_data = jsonable_encoder(sensors_in)
#     if len(sensors_in_data.trigger_types) > 0:
#         for trigger_type in sensors_in_data.trigger_types:
#             trigger_type_data.append(jsonable_encoder(trigger_type))
#     import pdb;pdb.set_trace()
#     # setattr()

#     sensors = Sensors(**sensors_in_data, packs_id=packs_id)
#     db_session.add(sensors)
#     db_session.commit()
#     db_session.refresh(sensors)
#     return sensors

# def sync(self, account_type, name, active, third_party, notes, identifier, custom_fields):
#         """
#         Syncs the account with the database. If account does not exist it is created. Other attributes
#         including account name are updated to conform with the third-party data source.
#         """
#         account_type_result = _get_or_create_account_type(account_type)

#         account = Account.query.filter(Account.identifier == identifier).first()

#         if not account:
#             account = Account()

#         account = self._populate_account(account, account_type_result.id, self.sanitize_account_name(name),
#                                          active, third_party, notes,
#                                          self.sanitize_account_identifier(identifier),
#                                          custom_fields)

#         db.session.add(account)
#         db.session.commit()
#         db.session.refresh(account)
#         account = self._load(account)
#         db.session.expunge(account)
#         return account


def get_sensor_entry_point(sensor_api_model):
    """Create a sensor entrypoint string from file_path and class_name

    Arguments:
        sensor_api_model {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    file_path = getattr(sensor_api_model, "artifact_uri", None)
    class_name = getattr(sensor_api_model, "class_name", None)
    packs_name = getattr(sensor_api_model, "packs_name", None)

    if packs_name == SYSTEM_PACK_NAME:
        # Special case for sensors which come included with the default installation
        entry_point = class_name
    else:
        module_path = file_path.split("/%s/" % (packs_name))[1]
        module_path = module_path.replace(os.path.sep, ".")
        module_path = module_path.replace(".py", "")
        entry_point = "%s.%s" % (module_path, class_name)

    return entry_point


def create(db_session: Session, *, sensors_in: SensorsCreate, packs_id: int) -> Sensors:
    sensors_in_data = jsonable_encoder(sensors_in)
    sensors = Sensors(**sensors_in_data, packs_id=packs_id)
    db_session.add(sensors)
    db_session.commit()
    db_session.refresh(sensors)
    return sensors


def update(
    db_session: Session, *, sensors: Sensors, sensors_in: SensorsUpdate
) -> Sensors:
    sensors_data = jsonable_encoder(sensors)
    update_data = sensors_in.dict(skip_defaults=True)
    for field in sensors_data:
        if field in update_data:
            setattr(sensors, field, update_data[field])
    db_session.add(sensors)
    db_session.commit()
    db_session.refresh(sensors)
    return sensors


# def create_or_update(db_session: Session, *, sensors_in: SensorsCreate, packs_id: int, sensors_id: int):
#     existing_sensors = get()


def remove(db_session: Session, *, sensors_id: int):
    sensors = db_session.query(Sensors).filter(Sensors.id == sensors_id).first()
    db_session.delete(sensors)
    db_session.commit()
    return sensors


# TODO: Add these as crud commands
# https://github.com/StackStorm/st2/blob/9edc3fb6da7f12515f6011960f1b72538e53368e/st2common/st2common/services/triggers.py
