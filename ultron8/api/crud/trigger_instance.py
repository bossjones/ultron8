from typing import List
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ultron8.api.db_models.trigger import TriggerInstanceDB

from ultron8.api.models.trigger import TriggerInstanceCreate
from ultron8.api.models.trigger import TriggerInstanceUpdate


def get(
    db_session: Session, *, trigger_instance_id: int
) -> Optional[TriggerInstanceDB]:
    """Return trigger object based on trigger id.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        id {int} -- ID of trigger

    Returns:
        Optional[TriggerInstanceDB] -- Returns a TriggerInstanceDB object or nothing if it doesn't exist
    """
    return (
        db_session.query(TriggerInstanceDB)
        .filter(TriggerInstanceDB.id == trigger_instance_id)
        .first()
    )


# def get_by_ref(db_session: Session, *, ref: str) -> Optional[TriggerInstanceDB]:
#     """Return trigger object based on trigger ref.

#     Arguments:
#         db_session {Session} -- SQLAlchemy Session object
#         ref {str} -- ref string

#     Returns:
#         Optional[TriggerInstanceDB] -- Returns a TriggerInstanceDB object or nothing if it doesn't exist
#     """
#     return (
#         db_session.query(TriggerInstanceDB).filter(TriggerInstanceDB.ref == ref).first()
#     )


def get_by_trigger(
    db_session: Session, *, trigger_instance_trigger: str
) -> Optional[TriggerInstanceDB]:
    """Return trigger object based on trigger trigger_instance_trigger.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        trigger_instance_trigger {str} -- trigger trigger_instance_trigger

    Returns:
        Optional[TriggerInstanceDB] -- Returns a TriggerInstanceDB object or nothing if it doesn't exist
    """
    return (
        db_session.query(TriggerInstanceDB)
        .filter(TriggerInstanceDB.trigger == trigger_instance_trigger)
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


def create(
    db_session: Session, *, trigger_instance_in: TriggerInstanceCreate
) -> TriggerInstanceDB:
    """Create TriggerInstanceDB object

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        trigger_instance_in {TriggerInstanceCreate} -- TriggerInstanceCreate object containing trigger args
        packs_id {int} -- Pack id

    Returns:
        TriggerInstanceDB -- Returns a TriggerInstanceDB object
    """
    trigger_instance_in_data = jsonable_encoder(trigger_instance_in)
    trigger_instance = TriggerInstanceDB(**trigger_instance_in_data)
    db_session.add(trigger_instance)
    db_session.commit()
    db_session.refresh(trigger_instance)
    return trigger_instance


def update(
    db_session: Session,
    *,
    trigger_instance: TriggerInstanceDB,
    trigger_instance_in: TriggerInstanceUpdate
) -> TriggerInstanceDB:
    """Update TriggerInstanceDB object

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        trigger_instance {TriggerInstanceDB} -- TriggerInstanceDB object
        trigger_instance_in {TriggerInstanceUpdate} -- TriggerInstanceDB object values to override

    Returns:
        TriggerInstanceDB -- Returns a TriggerInstanceDB object
    """
    trigger_instance_data = jsonable_encoder(trigger_instance)
    update_data = trigger_instance_in.dict(skip_defaults=True)
    for field in trigger_instance_data:
        if field in update_data:
            setattr(trigger_instance, field, update_data[field])
    db_session.add(trigger_instance)
    db_session.commit()
    db_session.refresh(trigger_instance)
    return trigger_instance


def remove(db_session: Session, *, trigger_instance_id: int):
    """Remove TriggerInstanceDB object

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        id {int} -- TriggerInstanceDB id

    Returns:
        [type] -- [description]
    """
    trigger_instance = (
        db_session.query(TriggerInstanceDB)
        .filter(TriggerInstanceDB.id == trigger_instance_id)
        .first()
    )
    db_session.delete(trigger_instance)
    db_session.commit()
    return trigger_instance
