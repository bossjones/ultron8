from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ultron8.api.core.security import get_password_hash, verify_password
from ultron8.api.db_models.action import Action
from ultron8.api.models.action import ActionCreate, ActionUpdate


def get(db_session: Session, *, action_id: int) -> Optional[Action]:
    return db_session.query(Action).filter(Action.id == action_id).first()


def get_by_ref(db_session: Session, *, ref: str) -> Optional[Action]:
    return db_session.query(Action).filter(Action.ref == ref).first()


def get_multi(db_session: Session, *, skip=0, limit=100) -> List[Optional[Action]]:
    return db_session.query(Action).offset(skip).limit(limit).all()


def get_multi_by_packs_id(
    db_session: Session, *, packs_id: int, skip=0, limit=100
) -> List[Optional[Action]]:
    return (
        db_session.query(Action)
        .filter(Action.packs_id == packs_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create(db_session: Session, *, action_in: ActionCreate, email: str) -> Action:
    action_in_data = jsonable_encoder(action_in)
    action = Action(**action_in_data, email=email)
    db_session.add(action)
    db_session.commit()
    db_session.refresh(action)
    return action


def update(db_session: Session, *, action: Action, action_in: ActionUpdate) -> Action:
    action_data = jsonable_encoder(action)
    update_data = action_in.dict(skip_defaults=True)
    for field in action_data:
        if field in update_data:
            setattr(action, field, update_data[field])
    db_session.add(action)
    db_session.commit()
    db_session.refresh(action)
    return action


def remove(db_session: Session, *, id: int):
    action = db_session.query(Action).filter(Action.id == id).first()
    db_session.delete(action)
    db_session.commit()
    return action
