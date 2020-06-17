"""Base Factory module."""

import factory

# from factory import alchemy
# from faker import Faker as RealFaker
# from faker.providers import internet, file, person, lorem, BaseProvider
from ultron8.api.db.u_sqlite.session import db_session

# # pylint: disable=invalid-name

# # class PackNameProvider(BaseProvider):
# #     def pack_name = (
# #         "ultron8", "nimrod", "jarvis", "friday", "eva", "adam"
# #     )

# pack_name = (
#     "ultron8", "nimrod", "jarvis", "friday", "eva", "adam"
# )

# pack_name_list = [
#     "ultron8", "nimrod", "jarvis", "friday", "eva", "adam"
# ]

# fake = RealFaker()
# fake.add_provider(internet)
# fake.add_provider(file)
# fake.add_provider(person)
# fake.add_provider(lorem)
# # fake.add_provider(PackNameProvider)

# NOTE: https://factoryboy.readthedocs.io/en/latest/reference.html?highlight=abstract#factory.FactoryOptions.abstract
class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        # This attribute indicates that the Factory subclass should not be used to generate objects, but instead provides some extra defaults.
        abstract = True
        # SQLAlchemy session to use to communicate with the database when creating an object through this SQLAlchemyModelFactory.
        sqlalchemy_session = db_session
        # Control the action taken by sqlalchemy session at the end of a create call.
        sqlalchemy_session_persistence = "commit"
