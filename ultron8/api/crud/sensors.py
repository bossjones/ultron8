from typing import List
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ultron8.api.core.security import get_password_hash
from ultron8.api.core.security import verify_password
from ultron8.api.db_models.sensors import Sensors
from ultron8.api.models.sensors import SensorsCreate
from ultron8.api.models.sensors import SensorsUpdate


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
