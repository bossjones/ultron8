from typing import List
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ultron8.api.db_models.trigger import TriggerTypeDB

from ultron8.api.models.trigger import TriggerTypeCreate
from ultron8.api.models.trigger import TriggerTypeUpdate


def get(db_session: Session, *, trigger_type_id: int) -> Optional[TriggerTypeDB]:
    """Return trigger object based on trigger id.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        id {int} -- ID of trigger

    Returns:
        Optional[TriggerTypeDB] -- Returns a TriggerTypeDB object or nothing if it doesn't exist
    """
    return (
        db_session.query(TriggerTypeDB)
        .filter(TriggerTypeDB.id == trigger_type_id)
        .first()
    )


def get_by_ref(db_session: Session, *, ref: str) -> Optional[TriggerTypeDB]:
    """Return trigger object based on trigger ref.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        ref {str} -- ref string

    Returns:
        Optional[TriggerTypeDB] -- Returns a TriggerTypeDB object or nothing if it doesn't exist
    """
    return db_session.query(TriggerTypeDB).filter(TriggerTypeDB.ref == ref).first()


def get_by_name(db_session: Session, *, name: str) -> Optional[TriggerTypeDB]:
    """Return trigger object based on trigger name.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        name {str} -- trigger name

    Returns:
        Optional[TriggerTypeDB] -- Returns a TriggerTypeDB object or nothing if it doesn't exist
    """
    return db_session.query(TriggerTypeDB).filter(TriggerTypeDB.name == name).first()


def get_multi(
    db_session: Session, *, skip=0, limit=100
) -> List[Optional[TriggerTypeDB]]:
    """Return list on TriggerTypeDB objects

    Arguments:
        db_session {Session} -- SQLAlchemy Session object

    Keyword Arguments:
        skip {int} -- Number of entries to skip (default: {0})
        limit {int} -- Number of trigger objects to limit by (default: {100})

    Returns:
        List[Optional[TriggerTypeDB]] -- Returns a list of TriggerTypeDB objects
    """
    return db_session.query(TriggerTypeDB).offset(skip).limit(limit).all()


def get_multi_by_packs_id(
    db_session: Session, *, packs_id: int, skip=0, limit=100
) -> List[Optional[TriggerTypeDB]]:
    """Get multiple TriggerTypeDB objects by packs_id

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        packs_id {int} -- Pack id

    Keyword Arguments:
        skip {int} -- Number of entries to skip (default: {0})
        limit {int} -- Number of trigger objects to limit by (default: {100})

    Returns:
        List[Optional[TriggerTypeDB]] -- Returns a list of TriggerTypeDB objects
    """
    return (
        db_session.query(TriggerTypeDB)
        .filter(TriggerTypeDB.packs_id == packs_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create(
    db_session: Session, *, trigger_type_in: TriggerTypeCreate, packs_id: int
) -> TriggerTypeDB:
    """Create TriggerTypeDB object

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        trigger_type_in {TriggerTypeCreate} -- TriggerTypeCreate object containing trigger args
        packs_id {int} -- Pack id

    Returns:
        TriggerTypeDB -- Returns a TriggerTypeDB object
    """
    trigger_type_in_data = jsonable_encoder(trigger_type_in)
    trigger = TriggerTypeDB(**trigger_type_in_data, packs_id=packs_id)
    db_session.add(trigger)
    db_session.commit()
    db_session.refresh(trigger)
    return trigger


def update(
    db_session: Session,
    *,
    trigger_type: TriggerTypeDB,
    trigger_type_in: TriggerTypeUpdate
) -> TriggerTypeDB:
    """[summary]

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        trigger {TriggerTypeDB} -- TriggerTypeDB object
        trigger_type_in {TriggerTypeUpdate} -- TriggerTypeDB object values to override

    Returns:
        TriggerTypeDB -- Returns a TriggerTypeDB object
    """
    trigger_data = jsonable_encoder(trigger_type)
    update_data = trigger_type_in.dict(skip_defaults=True)
    for field in trigger_data:
        if field in update_data:
            setattr(trigger_type, field, update_data[field])
    db_session.add(trigger_type)
    db_session.commit()
    db_session.refresh(trigger_type)
    return trigger_type


def remove(db_session: Session, *, trigger_type_id: int):
    """[summary]

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        id {int} -- TriggerTypeDB id

    Returns:
        [type] -- [description]
    """
    trigger = (
        db_session.query(TriggerTypeDB)
        .filter(TriggerTypeDB.id == trigger_type_id)
        .first()
    )
    db_session.delete(trigger)
    db_session.commit()
    return trigger
