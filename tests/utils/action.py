from tests.utils.packs import create_random_packs
from tests.utils.utils import random_lower_string
from ultron8.api import crud
from ultron8.api.db.u_sqlite.session import db_session
from ultron8.api.models.action import ActionCreate


# def create_random_action(packs_id: int = None):
#     if packs_id is None:
#         packs = create_random_packs()
#         packs_id = packs.id
#     title = random_lower_string()
#     description = random_lower_string()
#     actions_in = ActionCreate(title=title, description=description, id=id)
#     return crud.packs.create(db_session=db_session, actions_in=actions_in, packs_id=packs_id)
