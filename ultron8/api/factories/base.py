# """Base Factory module."""

# from factory import alchemy
# from faker import Faker as RealFaker
# from faker.providers import internet, file, person, lorem, BaseProvider
# from ultron8.api.db.u_sqlite.session import db_session

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

# class BaseFactory(alchemy.SQLAlchemyModelFactory):
#     class Meta:
#         abstract = True
#         sqlalchemy_session = db_session
#         sqlalchemy_session_persistence = "commit"
