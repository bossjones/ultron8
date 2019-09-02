from typing import List
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ultron8.api.db_models.trigger import TriggerDB

from ultron8.api.models.trigger import TriggerCreate
from ultron8.api.models.trigger import TriggerUpdate

from ultron8.exceptions.db import (
    UltronDBObjectNotFoundError,
    UltronDBObjectNotFoundError,
)

import logging
import ujson

LOG = logging.getLogger(__name__)

# __all__ = [
#     'add_trigger_models',

#     'get_trigger_db_by_ref',
#     'get_by_id',
#     'get_by_uid',
#     'get_trigger_db_by_ref_or_dict',
#     'get_trigger_db_given_type_and_params',
#     'get_trigger_type_db',

#     'create_trigger_db',
#     'create_trigger_type_db',

#     'create_or_update_trigger_db',
#     'create_or_update_trigger_type_db'
# ]


def get(db_session: Session, *, trigger_id: int) -> Optional[TriggerDB]:
    """Return trigger object based on trigger id.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        id {int} -- ID of trigger

    Returns:
        Optional[TriggerDB] -- Returns a TriggerDB object or nothing if it doesn't exist
    """
    return db_session.query(TriggerDB).filter(TriggerDB.id == trigger_id).first()


def get_by_ref(db_session: Session, *, ref: str) -> Optional[TriggerDB]:
    """Return trigger object based on trigger ref.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        ref {str} -- ref string

    Returns:
        Optional[TriggerDB] -- Returns a TriggerDB object or nothing if it doesn't exist
    """
    return db_session.query(TriggerDB).filter(TriggerDB.ref == ref).first()


def get_by_id(db_session: Session, *, id: int) -> Optional[TriggerDB]:
    """Return trigger object based on trigger id.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        id {int} -- id int

    Returns:
        Optional[TriggerDB] -- Returns a TriggerDB object or nothing if it doesn't exist
    """
    return db_session.query(TriggerDB).filter(TriggerDB.id == id).first()


def get_by_uid(db_session: Session, *, uid: int) -> Optional[TriggerDB]:
    """Return trigger object based on trigger uid.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        uid {int} -- uid int

    Returns:
        Optional[TriggerDB] -- Returns a TriggerDB object or nothing if it doesn't exist
    """
    return db_session.query(TriggerDB).filter(TriggerDB.uid == uid).first()


def get_by_name(db_session: Session, *, name: str) -> Optional[TriggerDB]:
    """Return trigger object based on trigger name.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        name {str} -- trigger name

    Returns:
        Optional[TriggerDB] -- Returns a TriggerDB object or nothing if it doesn't exist
    """
    return db_session.query(TriggerDB).filter(TriggerDB.name == name).first()


def get_trigger_db_given_type_and_params(
    db_session: Session, *, type: str, parameters: dict
) -> Optional[TriggerDB]:
    """Return trigger object based on type and params

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        type {str} -- trigger type name
        parameters {dict} -- trigger parameters

    Returns:
        Optional[TriggerDB] -- Returns a TriggerDB object or nothing if it doesn't exist
    """
    try:
        parameters = parameters or {}
        parameters_str = ujson.dumps(parameters)
        trigger_dbs = (
            db_session.query(TriggerDB)
            .filter(TriggerDB.type == type, TriggerDB.parameters == parameters_str)
            .all()
        )

        trigger_db = trigger_dbs[0] if len(trigger_dbs) > 0 else None

        if not parameters and not trigger_db:
            # We need to do double query because some TriggeDB objects without
            # parameters have "parameters" attribute stored in the db and others
            # don't
            trigger_db = (
                db_session.query(TriggerDB)
                .filter(TriggerDB.type == type, TriggerDB.parameters == None)
                .first()
            )

        return trigger_db
    except UltronDBObjectNotFoundError as e:
        LOG.debug(
            'Database lookup for type="%s" parameters="%s" resulted '
            + "in exception : %s.",
            type,
            parameters,
            e,
            exc_info=True,
        )
        return None


def get_trigger_db_by_ref_or_dict(
    db_session: Session, *, trigger: TriggerCreate
) -> Optional[TriggerDB]:
    """
    Retrieve TriggerDB object based on the trigger reference of based on a
    provided dictionary with trigger attributes.
    """
    # TODO: This is nasty, this should take a unique reference and not a dict
    if isinstance(trigger.ref, str):
        trigger_db = get_by_ref(db_session, ref=trigger.ref)
    else:
        # If id / uid is available we try to look up Trigger by id. This way we can avoid bug in
        # pymongo / mongoengine related to "parameters" dictionary lookups
        trigger_id = trigger.id
        trigger_uid = trigger.uid

        # TODO: Remove parameters dictionary look up when we can confirm each trigger dictionary
        # passed to this method always contains id or uid
        if trigger_id:
            LOG.debug("Looking up TriggerDB by id: %s", trigger_id)
            trigger_db = get_by_id(db_session, id=trigger_id)
        elif trigger_uid:
            LOG.debug("Looking up TriggerDB by uid: %s", trigger_uid)
            trigger_db = get_by_uid(db_session, uid=trigger_uid)
        else:
            # Last resort - look it up by parameters
            trigger_type = trigger.type
            parameters = trigger.parameters

            LOG.debug(
                "Looking up TriggerDB by type and parameters: type=%s, parameters=%s",
                trigger_type,
                parameters,
            )
            trigger_db = get_trigger_db_given_type_and_params(
                db_session, type=trigger_type, parameters=parameters
            )

    return trigger_db


def _get_trigger_db(
    db_session: Session, *, trigger: TriggerCreate
) -> Optional[TriggerDB]:
    # TODO: This method should die in a fire
    # XXX: Do not make this method public.

    if isinstance(trigger, TriggerCreate):
        name = trigger.name
        packs_name = trigger.packs_name

        if name and packs_name:
            ref = "{}.{}".format(packs_name, name)
            return get_by_ref(db_session, ref=ref)
        return get_trigger_db_given_type_and_params(
            db_session, type=trigger.type, parameters=trigger.parameters
        )
    else:
        raise Exception("Unrecognized object")


def get_trigger_type_db(db_session: Session, *, ref: str) -> Optional[TriggerDB]:
    """
    Returns the trigger type object from db given a string ref.

    :param ref: Reference to the trigger type db object.
    :type ref: ``str``

    :rtype trigger_type: ``object``
    """
    try:
        return get_by_ref(db_session, ref=ref)
    except UltronDBObjectNotFoundError as e:
        LOG.debug(
            'Database lookup for ref="%s" resulted ' + "in exception : %s.",
            ref,
            e,
            exc_info=True,
        )

    return None


# TODO: Enable this
# def _get_trigger_dict_given_rule(rule):
#     trigger = rule.trigger
#     trigger_dict = {}
#     triggertype_ref = ResourceReference.from_string_reference(trigger.get('type'))
#     trigger_dict['pack'] = trigger_dict.get('pack', triggertype_ref.pack)
#     trigger_dict['type'] = triggertype_ref.ref
#     trigger_dict['parameters'] = rule.trigger.get('parameters', {})

#     return trigger_dict

# def create_trigger_db(db_session: Session, *, trigger: TriggerCreate) -> Optional[TriggerDB]:
#     # TODO: This is used only in trigger API controller. We should get rid of this.
#     trigger_ref = "{}.{}".format(trigger.packs_name, trigger.name)
#     trigger_db = get_by_ref(db_session, ref=trigger.ref)
#     # TODO: Enable this
#     # if not trigger_db:
#     #     trigger_db = TriggerAPI.to_model(trigger_api)
#     #     LOG.debug('Verified trigger and formulated TriggerDB=%s', trigger_db)
#     #     trigger_db = Trigger.add_or_update(trigger_db)
#     # return trigger_db


# def create_or_update_trigger_db(trigger, log_not_unique_error_as_debug=False):
#     """
#     Create a new TriggerDB model if one doesn't exist yet or update existing
#     one.

#     :param trigger: Trigger info.
#     :type trigger: ``dict``
#     """
#     assert isinstance(trigger, dict)

#     existing_trigger_db = _get_trigger_db(trigger)

#     if existing_trigger_db:
#         is_update = True
#     else:
#         is_update = False

#     trigger_api = TriggerAPI(**trigger)
#     trigger_api.validate()
#     trigger_db = TriggerAPI.to_model(trigger_api)

#     if is_update:
#         trigger_db.id = existing_trigger_db.id

#     trigger_db = Trigger.add_or_update(trigger_db,
#         log_not_unique_error_as_debug=log_not_unique_error_as_debug)

#     extra = {'trigger_db': trigger_db}

#     if is_update:
#         LOG.audit('Trigger updated. Trigger.id=%s' % (trigger_db.id), extra=extra)
#     else:
#         LOG.audit('Trigger created. Trigger.id=%s' % (trigger_db.id), extra=extra)

#     return trigger_db


# def create_trigger_db_from_rule(rule):
#     trigger_dict = _get_trigger_dict_given_rule(rule)
#     existing_trigger_db = _get_trigger_db(trigger_dict)
#     # For simple triggertypes (triggertype with no parameters), we create a trigger when
#     # registering triggertype. So if we hit the case that there is no trigger in db but
#     # parameters is empty, then this case is a run time error.
#     if not trigger_dict.get('parameters', {}) and not existing_trigger_db:
#         raise TriggerDoesNotExistException(
#             'A simple trigger should have been created when registering '
#             'triggertype. Cannot create trigger: %s.' % (trigger_dict))

#     if not existing_trigger_db:
#         trigger_db = create_or_update_trigger_db(trigger_dict)
#     else:
#         trigger_db = existing_trigger_db

#     # Special reference counting for trigger with parameters.
#     # if trigger_dict.get('parameters', None):
#     #     Trigger.update(trigger_db, inc__ref_count=1)

#     return trigger_db


# def increment_trigger_ref_count(rule_api):
#     """
#     Given the rule figures out the TriggerType with parameter and increments
#     reference count on the appropriate Trigger.

#     :param rule_api: Rule object used to infer the Trigger.
#     :type rule_api: ``RuleApi``
#     """
#     trigger_dict = _get_trigger_dict_given_rule(rule_api)

#     # Special reference counting for trigger with parameters.
#     if trigger_dict.get('parameters', None):
#         trigger_db = _get_trigger_db(trigger_dict)
#         Trigger.update(trigger_db, inc__ref_count=1)


# def cleanup_trigger_db_for_rule(rule_db):
#     # rule.trigger is actually trigger_db ref.
#     existing_trigger_db = get_trigger_db_by_ref(rule_db.trigger)
#     if not existing_trigger_db or not existing_trigger_db.parameters:
#         # nothing to be done here so moving on.
#         LOG.debug('ref_count decrement for %s not required.', existing_trigger_db)
#         return
#     Trigger.update(existing_trigger_db, dec__ref_count=1)
#     Trigger.delete_if_unreferenced(existing_trigger_db)


def get_multi(db_session: Session, *, skip=0, limit=100) -> List[Optional[TriggerDB]]:
    """Return list on TriggerDB objects

    Arguments:
        db_session {Session} -- SQLAlchemy Session object

    Keyword Arguments:
        skip {int} -- Number of entries to skip (default: {0})
        limit {int} -- Number of trigger objects to limit by (default: {100})

    Returns:
        List[Optional[TriggerDB]] -- Returns a list of TriggerDB objects
    """
    return db_session.query(TriggerDB).offset(skip).limit(limit).all()


def get_multi_by_packs_id(
    db_session: Session, *, packs_id: int, skip=0, limit=100
) -> List[Optional[TriggerDB]]:
    """Get multiple TriggerDB objects by packs_id

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        packs_id {int} -- Pack id

    Keyword Arguments:
        skip {int} -- Number of entries to skip (default: {0})
        limit {int} -- Number of trigger objects to limit by (default: {100})

    Returns:
        List[Optional[TriggerDB]] -- Returns a list of TriggerDB objects
    """
    return (
        db_session.query(TriggerDB)
        .filter(TriggerDB.packs_id == packs_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create(
    db_session: Session, *, trigger_in: TriggerCreate, packs_id: int
) -> TriggerDB:
    """Create TriggerDB object

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        trigger_in {TriggerCreate} -- TriggerCreate object containing trigger args
        packs_id {int} -- Pack id

    Returns:
        TriggerDB -- Returns a TriggerDB object
    """
    # import pdb;pdb.set_trace()
    trigger_in_data = jsonable_encoder(trigger_in)
    trigger = TriggerDB(**trigger_in_data, packs_id=packs_id)
    db_session.add(trigger)
    db_session.commit()
    db_session.refresh(trigger)
    return trigger


def update(
    db_session: Session, *, trigger: TriggerDB, trigger_in: TriggerUpdate
) -> TriggerDB:
    """[summary]

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        trigger {TriggerDB} -- TriggerDB object
        trigger_in {TriggerUpdate} -- TriggerDB object values to override

    Returns:
        TriggerDB -- Returns a TriggerDB object
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


def remove(db_session: Session, *, trigger_id: int) -> TriggerDB:
    """[summary]

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        id {int} -- TriggerDB id

    Returns:
        [type] -- [description]
    """
    trigger = db_session.query(TriggerDB).filter(TriggerDB.id == trigger_id).first()
    db_session.delete(trigger)
    db_session.commit()
    return trigger
