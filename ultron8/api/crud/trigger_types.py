from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ultron8.api.db_models.trigger import TriggerTypeDB
from ultron8.api.models.trigger import TriggerTypeCreate, TriggerTypeUpdate

# from ultron8.api.models.system.common import ResourceReference


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
    db_session: Session, *, skip: int = 0, limit: int = 100
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
    db_session: Session, *, packs_id: int, skip: int = 0, limit: int = 100
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


# SOURCE: st2common/st2common/services/triggers.py
# def _create_trigger_type(pack, name, description=None, payload_schema=None,
#                          parameters_schema=None, tags=None, metadata_file=None):
#     trigger_type = {
#         'name': name,
#         'pack': pack,
#         'description': description,
#         'payload_schema': payload_schema,
#         'parameters_schema': parameters_schema,
#         'tags': tags,
#         'metadata_file': metadata_file
#     }

#     return create_or_update_trigger_type_db(trigger_type=trigger_type)


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
    # TODO: missing packs_name
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
    update_data = trigger_type_in.dict(exclude_unset=True)
    for field in trigger_data:
        if field in update_data:
            setattr(trigger_type, field, update_data[field])
    db_session.add(trigger_type)
    db_session.commit()
    db_session.refresh(trigger_type)
    return trigger_type


# # NOTE: idea borrowed from create_or_update_trigger_type_db
# def create_or_update(
#     db_session: Session, *, trigger_type_in: TriggerTypeUpdate, packs_id: int
# ) -> TriggerTypeDB:

#     # validation is automatically handled by pydantic

#     # create ref string
#     ref = "{}.{}".format(trigger_type_in.packs_name, trigger_type_in.name)

#     # check if already exists in database

#     existing_trigger_type_db = get_by_ref(ref)

#     # If we get a real object back,
#     if existing_trigger_type_db:
#         is_update = True
#     else:
#         is_update = False

#     # if object exists in db, make sure the ID is set
#     if is_update:
#         trigger_type_api.id = existing_trigger_type_db.id

#     pass


def remove(db_session: Session, *, trigger_type_id: int) -> TriggerTypeDB:
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


# https://github.com/StackStorm/st2/blob/9edc3fb6da7f12515f6011960f1b72538e53368e/st2common/st2common/models/utils/sensor_type_utils.py
# https://github.com/StackStorm/st2/blob/9edc3fb6da7f12515f6011960f1b72538e53368e/st2common/st2common/services/triggers.py
