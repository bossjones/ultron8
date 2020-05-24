from sqlalchemy.orm import Session

from tests.utils.user import create_random_user
from tests.utils.utils import random_lower_string
from ultron8.api import crud
from ultron8.api.models.item import ItemCreate


def create_random_item(db: Session, owner_id: int = None):
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description, id=id)
    return crud.item.create(db_session=db, item_in=item_in, owner_id=owner_id)
