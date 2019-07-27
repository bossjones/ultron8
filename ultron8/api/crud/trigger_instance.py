from typing import List
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ultron8.api.db_models.trigger import TriggerInstanceDB

from ultron8.api.models.trigger import TriggerInstanceCreate
from ultron8.api.models.trigger import TriggerInstanceUpdate


def get(db_session: Session, *, trigger_id: int) -> Optional[TriggerInstanceDB]:
    """Return trigger object based on trigger id.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        id {int} -- ID of trigger

    Returns:
        Optional[TriggerInstanceDB] -- Returns a TriggerInstanceDB object or nothing if it doesn't exist
    """
    return (
        db_session.query(TriggerInstanceDB)
        .filter(TriggerInstanceDB.id == trigger_id)
        .first()
    )


def get_by_ref(db_session: Session, *, ref: str) -> Optional[TriggerInstanceDB]:
    """Return trigger object based on trigger ref.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        ref {str} -- ref string

    Returns:
        Optional[TriggerInstanceDB] -- Returns a TriggerInstanceDB object or nothing if it doesn't exist
    """
    return (
        db_session.query(TriggerInstanceDB).filter(TriggerInstanceDB.ref == ref).first()
    )


def get_by_name(db_session: Session, *, name: str) -> Optional[TriggerInstanceDB]:
    """Return trigger object based on trigger name.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        name {str} -- trigger name

    Returns:
        Optional[TriggerInstanceDB] -- Returns a TriggerInstanceDB object or nothing if it doesn't exist
    """
    return (
        db_session.query(TriggerInstanceDB)
        .filter(TriggerInstanceDB.name == name)
        .first()
    )


def get_multi(
    db_session: Session, *, skip=0, limit=100
) -> List[Optional[TriggerInstanceDB]]:
    """Return list on TriggerInstanceDB objects

    Arguments:
        db_session {Session} -- SQLAlchemy Session object

    Keyword Arguments:
        skip {int} -- Number of entries to skip (default: {0})
        limit {int} -- Number of trigger objects to limit by (default: {100})

    Returns:
        List[Optional[TriggerInstanceDB]] -- Returns a list of TriggerInstanceDB objects
    """
    return db_session.query(TriggerInstanceDB).offset(skip).limit(limit).all()


def get_multi_by_packs_id(
    db_session: Session, *, packs_id: int, skip=0, limit=100
) -> List[Optional[TriggerInstanceDB]]:
    """Get multiple TriggerInstanceDB objects by packs_id

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        packs_id {int} -- Pack id

    Keyword Arguments:
        skip {int} -- Number of entries to skip (default: {0})
        limit {int} -- Number of trigger objects to limit by (default: {100})

    Returns:
        List[Optional[TriggerInstanceDB]] -- Returns a list of TriggerInstanceDB objects
    """
    return (
        db_session.query(TriggerInstanceDB)
        .filter(TriggerInstanceDB.packs_id == packs_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create(
    db_session: Session, *, trigger_in: TriggerInstanceCreate, packs_id: int
) -> TriggerInstanceDB:
    """Create TriggerInstanceDB object

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        trigger_in {TriggerInstanceCreate} -- TriggerInstanceCreate object containing trigger args
        packs_id {int} -- Pack id

    Returns:
        TriggerInstanceDB -- Returns a TriggerInstanceDB object
    """
    trigger_in_data = jsonable_encoder(trigger_in)
    trigger = TriggerInstanceDB(**trigger_in_data, packs_id=packs_id)
    db_session.add(trigger)
    db_session.commit()
    db_session.refresh(trigger)
    return trigger


def update(
    db_session: Session,
    *,
    trigger: TriggerInstanceDB,
    trigger_in: TriggerInstanceUpdate
) -> TriggerInstanceDB:
    """[summary]

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        trigger {TriggerInstanceDB} -- TriggerInstanceDB object
        trigger_in {TriggerInstanceUpdate} -- TriggerInstanceDB object values to override

    Returns:
        TriggerInstanceDB -- Returns a TriggerInstanceDB object
    """
    trigger_data = jsonable_encoder(trigger)
    update_data = trigger_in.dict(skip_defaults=True)
    for field in trigger_data:
        if field in update_data:
            setattr(trigger, field, update_data[field])
    db_session.add(trigger)
    db_session.commit()
    db_session.refresh(trigger)
    return trigger


def remove(db_session: Session, *, trigger_id: int):
    """[summary]

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        id {int} -- TriggerInstanceDB id

    Returns:
        [type] -- [description]
    """
    trigger = (
        db_session.query(TriggerInstanceDB)
        .filter(TriggerInstanceDB.id == trigger_id)
        .first()
    )
    db_session.delete(trigger)
    db_session.commit()
    return trigger