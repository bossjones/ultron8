from typing import List
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ultron8.api.db_models.packs import Packs
from ultron8.api.models.packs import PacksCreate
from ultron8.api.models.packs import PacksUpdate
from sqlalchemy.orm.session import Session


def get(db_session: Session, *, packs_id: int) -> Optional[Packs]:
    """Return Packs object based on pack id.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        packs_id {int} -- ID of pack

    Returns:
        Optional[Packs] -- Returns a Packs object or nothing if it doesn't exist
    """
    return db_session.query(Packs).filter(Packs.id == packs_id).first()


def get_by_ref(db_session: Session, *, ref: str) -> Optional[Packs]:
    """Return Packs object based on pack ref.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        ref {str} -- ref name of pack

    Returns:
        Optional[Packs] -- Returns a Packs object or nothing if it doesn't exist
    """
    return db_session.query(Packs).filter(Packs.ref == ref).first()


def get_by_name(db_session: Session, *, name: str) -> Optional[Packs]:
    """Return Packs object based on pack name.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        name {str} -- name of pack

    Returns:
        Optional[Packs] -- Returns a Packs object or nothing if it doesn't exist
    """
    return db_session.query(Packs).filter(Packs.name == name).first()


def get_multi(db_session: Session, *, skip=0, limit=100) -> List[Optional[Packs]]:
    """Return multiple Packs objects.

    Arguments:
        db_session {Session} -- SQLAlchemy Session object
        name {str} -- name of pack

    Returns:
        Optional[Packs] -- Returns a Packs object or nothing if it doesn't exist
    """
    return db_session.query(Packs).offset(skip).limit(limit).all()


def create(db_session: Session, *, packs_in: PacksCreate) -> Packs:
    packs_in_data = jsonable_encoder(packs_in)
    packs = Packs(**packs_in_data)
    db_session.add(packs)
    db_session.commit()
    db_session.refresh(packs)
    return packs


def update(db_session: Session, *, packs: Packs, packs_in: PacksUpdate) -> Packs:
    packs_data = jsonable_encoder(packs)
    update_data = packs_in.dict(skip_defaults=True)
    for field in packs_data:
        if field in update_data:
            setattr(packs, field, update_data[field])
    db_session.add(packs)
    db_session.commit()
    db_session.refresh(packs)
    return packs


def remove(db_session: Session, *, id: int) -> Packs:
    packs = db_session.query(Packs).filter(Packs.id == id).first()
    db_session.delete(packs)
    db_session.commit()
    return packs
