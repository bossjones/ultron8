from typing import List
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ultron8.api.db_models.packs import Packs
from ultron8.api.models.packs import PacksCreate
from ultron8.api.models.packs import PacksUpdate


def get(db_session: Session, *, packs_id: int) -> Optional[Packs]:
    return db_session.query(Packs).filter(Packs.id == packs_id).first()


def get_by_ref(db_session: Session, *, ref: str) -> Optional[Packs]:
    return db_session.query(Packs).filter(Packs.ref == ref).first()


def get_multi(db_session: Session, *, skip=0, limit=100) -> List[Optional[Packs]]:
    return db_session.query(Packs).offset(skip).limit(limit).all()


# def get_multi_by_email(
#     db_session: Session, *, email: str, skip=0, limit=100
# ) -> List[Optional[Packs]]:
#     return (
#         db_session.query(Packs)
#         .filter(Packs.email == email)
#         .offset(skip)
#         .limit(limit)
#         .all()
#     )


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


def remove(db_session: Session, *, id: int):
    packs = db_session.query(Packs).filter(Packs.id == id).first()
    db_session.delete(packs)
    db_session.commit()
    return packs
