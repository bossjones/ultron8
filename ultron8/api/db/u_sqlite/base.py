# Import all the models, so that Base has them before being
# imported by Alembic
from ultron8.api.db.u_sqlite.base_class import Base  # noqa
from ultron8.api.db_models.guid import Guid  # noqa
from ultron8.api.db_models.item import Item  # noqa
from ultron8.api.db_models.user import User  # noqa
from ultron8.api.db_models.packs import Packs  # noqa
from ultron8.api.db_models.action import Action  # noqa

# from ultron8.api.db_models.item import Item  # noqa

# smoke tests
if "__main__" == __name__:
    guid = Guid()

    print(guid)

    user = User()

    print(user)

    item = Item()

    print(item)
