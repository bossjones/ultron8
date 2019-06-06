from ultron8.api.db.u_sqlite import database, guid_tracker
from sqlalchemy import and_
from collections import namedtuple
from datetime import datetime
import logging
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ultron8.api.db_models.item import Item
from ultron8.api.models.item import ItemCreate, ItemUpdate


def get(db_session: Session, *, id: int) -> Optional[Item]:
    return db_session.query(Item).filter(Item.id == id).first()


def get_multi(db_session: Session, *, skip=0, limit=100) -> List[Optional[Item]]:
    return db_session.query(Item).offset(skip).limit(limit).all()


def get_multi_by_owner(
    db_session: Session, *, owner_id: int, skip=0, limit=100
) -> List[Optional[Item]]:
    return (
        db_session.query(Item)
        .filter(Item.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create(db_session: Session, *, item_in: ItemCreate, owner_id: int) -> Item:
    item_in_data = jsonable_encoder(item_in)
    item = Item(**item_in_data, owner_id=owner_id)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    return item


def update(db_session: Session, *, item: Item, item_in: ItemUpdate) -> Item:
    item_data = jsonable_encoder(item)
    update_data = item_in.dict(skip_defaults=True)
    for field in item_data:
        if field in update_data:
            setattr(item, field, update_data[field])
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    return item


def remove(db_session: Session, *, id: int):
    item = db_session.query(Item).filter(Item.id == id).first()
    db_session.delete(item)
    db_session.commit()
    return item


"""Collection of db transactions."""
# pylint:disable=no-value-for-parameter


log = logging.getLogger(__name__)


@database.transaction()
async def retrieve_guid_record(guid):
    """Retrieve a record by guid."""
    # Get guid
    query = guid_tracker.select().where(
        and_(guid_tracker.c.id == guid, guid_tracker.c.expire > datetime.now())
    )

    return await database.fetch_one(query)


@database.transaction()
async def create_guid_record(guid: str, name: str, expire: datetime) -> bool:
    """Create a name value with a guid as the pk."""
    # Clean old guids
    clean_query = guid_tracker.delete().where(
        and_(guid_tracker.c.expire < datetime.now())
    )
    await database.execute(clean_query)

    # Add new guid
    query = guid_tracker.insert().values(id=guid, expire=expire, name=name)
    await database.execute(query)

    return True


@database.transaction()
async def update_guid_record(guid: str, name: str = None, expire: datetime = None):
    """Update a name value with a guid as the pk."""
    # Clean old guids
    clean_query = guid_tracker.delete().where(
        and_(guid_tracker.c.expire < datetime.now())
    )
    await database.execute(clean_query)

    # Update guids
    update = {}
    if expire:
        update["expire"] = expire
    if name:
        update["name"] = name

    update_query = (
        guid_tracker.update().values(**update).where(guid_tracker.c.id == guid)
    )
    await database.execute(update_query)

    # Get current guid
    query = guid_tracker.select().where(
        and_(guid_tracker.c.id == guid, guid_tracker.c.expire > datetime.now())
    )

    return await database.fetch_one(query)


@database.transaction()
async def delete_guid_record(guid):
    """Delete a guid record."""
    query = guid_tracker.delete().where(guid_tracker.c.id == guid)
    await database.execute(query)
