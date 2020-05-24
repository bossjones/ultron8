from typing import List
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ultron8.api.db_models.trigger import TriggerTagsDB

from ultron8.api.models.trigger import TriggerTagsCreate
from ultron8.api.models.trigger import TriggerTagsUpdate


def get(db_session: Session, *, trigger_id: int) -> Optional[TriggerTagsDB]:
    """Return trigger object based on trigger id.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        id {int} -- ID of trigger

    Returns:
        Optional[TriggerTagsDB] -- Returns a TriggerTagsDB object or nothing if it doesn't exist
    """
    return (
        db_session.query(TriggerTagsDB).filter(TriggerTagsDB.id == trigger_id).first()
    )


def get_by_ref(db_session: Session, *, ref: str) -> Optional[TriggerTagsDB]:
    """Return trigger object based on trigger ref.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        ref {str} -- ref string

    Returns:
        Optional[TriggerTagsDB] -- Returns a TriggerTagsDB object or nothing if it doesn't exist
    """
    return db_session.query(TriggerTagsDB).filter(TriggerTagsDB.ref == ref).first()


def get_by_name(db_session: Session, *, name: str) -> Optional[TriggerTagsDB]:
    """Return trigger object based on trigger name.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        name {str} -- trigger name

    Returns:
        Optional[TriggerTagsDB] -- Returns a TriggerTagsDB object or nothing if it doesn't exist
    """
    return db_session.query(TriggerTagsDB).filter(TriggerTagsDB.name == name).first()


def get_multi(
    db_session: Session, *, skip=0, limit=100
) -> List[Optional[TriggerTagsDB]]:
    """Return list on TriggerTagsDB objects

    Arguments:
        db_session {Session} -- SQLAlchemy Session object

    Keyword Arguments:
        skip {int} -- Number of entries to skip (default: {0})
        limit {int} -- Number of trigger objects to limit by (default: {100})

    Returns:
        List[Optional[TriggerTagsDB]] -- Returns a list of TriggerTagsDB objects
    """
    return db_session.query(TriggerTagsDB).offset(skip).limit(limit).all()


def get_multi_by_packs_id(
    db_session: Session, *, packs_id: int, skip=0, limit=100
) -> List[Optional[TriggerTagsDB]]:
    """Get multiple TriggerTagsDB objects by packs_id

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        packs_id {int} -- Pack id

    Keyword Arguments:
        skip {int} -- Number of entries to skip (default: {0})
        limit {int} -- Number of trigger objects to limit by (default: {100})

    Returns:
        List[Optional[TriggerTagsDB]] -- Returns a list of TriggerTagsDB objects
    """
    return (
        db_session.query(TriggerTagsDB)
        .filter(TriggerTagsDB.packs_id == packs_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create(
    db_session: Session, *, trigger_in: TriggerTagsCreate, packs_id: int
) -> TriggerTagsDB:
    """Create TriggerTagsDB object

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        trigger_in {TriggerTagsCreate} -- TriggerTagsCreate object containing trigger args
        packs_id {int} -- Pack id

    Returns:
        TriggerTagsDB -- Returns a TriggerTagsDB object
    """
    trigger_in_data = jsonable_encoder(trigger_in)
    trigger = TriggerTagsDB(**trigger_in_data, packs_id=packs_id)
    db_session.add(trigger)
    db_session.commit()
    db_session.refresh(trigger)
    return trigger


def update(
    db_session: Session, *, trigger: TriggerTagsDB, trigger_in: TriggerTagsUpdate
) -> TriggerTagsDB:
    """[summary]

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        trigger {TriggerTagsDB} -- TriggerTagsDB object
        trigger_in {TriggerTagsUpdate} -- TriggerTagsDB object values to override

    Returns:
        TriggerTagsDB -- Returns a TriggerTagsDB object
    """
    trigger_data = jsonable_encoder(trigger)
    update_data = trigger_in.dict(exclude_unset=True)
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
        id {int} -- TriggerTagsDB id

    Returns:
        [type] -- [description]
    """
    trigger = (
        db_session.query(TriggerTagsDB).filter(TriggerTagsDB.id == trigger_id).first()
    )
    db_session.delete(trigger)
    db_session.commit()
    return trigger
