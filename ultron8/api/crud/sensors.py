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


def create(db_session: Session, *, sensors_in: SensorsCreate) -> Sensors:
    sensors_in_data = jsonable_encoder(sensors_in)
    sensors = Sensors(**sensors_in_data)
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


def remove(db_session: Session, *, id: int):
    sensors = db_session.query(Sensors).filter(Sensors.id == id).first()
    db_session.delete(sensors)
    db_session.commit()
    return sensors
