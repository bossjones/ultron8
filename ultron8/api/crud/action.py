from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.orm.session import Session

# from ultron8.api.core.security import get_password_hash
# from ultron8.api.core.security import verify_password
# from ultron8.api.db_models.packs import Packs
from ultron8.api.db_models.action import Action
from ultron8.api.models.action import ActionCreate, ActionUpdate


def get(db_session: Session, *, action_id: int) -> Optional[Action]:
    """Return action object based on action id.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        action_id {int} -- ID of action

    Returns:
        Optional[Action] -- Returns a Action object or nothing if it doesn't exist
    """
    return db_session.query(Action).filter(Action.id == action_id).first()


def get_by_ref(db_session: Session, *, ref: str) -> Optional[Action]:
    """Return action object based on action ref.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        ref {str} -- ref string

    Returns:
        Optional[Action] -- Returns a Action object or nothing if it doesn't exist
    """
    return db_session.query(Action).filter(Action.ref == ref).first()


def get_by_name(db_session: Session, *, name: str) -> Optional[Action]:
    """Return action object based on action name.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        name {str} -- action name

    Returns:
        Optional[Action] -- Returns a Action object or nothing if it doesn't exist
    """
    return db_session.query(Action).filter(Action.name == name).first()


def get_multi(db_session: Session, *, skip=0, limit=100) -> List[Optional[Action]]:
    """Return list on Action objects

    Arguments:
        db_session {Session} -- SQLAlchemy Session object

    Keyword Arguments:
        skip {int} -- Number of entries to skip (default: {0})
        limit {int} -- Number of action objects to limit by (default: {100})

    Returns:
        List[Optional[Action]] -- Returns a list of Action objects
    """
    return db_session.query(Action).offset(skip).limit(limit).all()


def get_multi_by_packs_id(
    db_session: Session, *, packs_id: int, skip=0, limit=100
) -> List[Optional[Action]]:
    """Get multiple Action objects by packs_id

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        packs_id {int} -- Pack id

    Keyword Arguments:
        skip {int} -- Number of entries to skip (default: {0})
        limit {int} -- Number of action objects to limit by (default: {100})

    Returns:
        List[Optional[Action]] -- Returns a list of Action objects
    """
    return (
        db_session.query(Action)
        .filter(Action.packs_id == packs_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create(db_session: Session, *, action_in: ActionCreate, packs_id: int) -> Action:
    """Create Action object

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        action_in {ActionCreate} -- ActionCreate object containing action args
        packs_id {int} -- Pack id

    Returns:
        Action -- Returns a Action object
    """
    action_in_data = jsonable_encoder(action_in)
    action = Action(**action_in_data, packs_id=packs_id)
    db_session.add(action)
    db_session.commit()
    db_session.refresh(action)
    return action


def update(db_session: Session, *, action: Action, action_in: ActionUpdate) -> Action:
    """[summary]

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        action {Action} -- Action object
        action_in {ActionUpdate} -- Action object values to override

    Returns:
        Action -- Returns a Action object
    """
    action_data = jsonable_encoder(action)
    update_data = action_in.dict(exclude_unset=True)
    for field in action_data:
        if field in update_data:
            setattr(action, field, update_data[field])
    db_session.add(action)
    db_session.commit()
    db_session.refresh(action)
    return action


def remove(db_session: Session, *, action_id: int) -> Action:
    """[summary]

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        action_id {int} -- Action id

    Returns:
        [type] -- [description]
    """
    action = db_session.query(Action).filter(Action.id == action_id).first()
    db_session.delete(action)
    db_session.commit()
    return action
