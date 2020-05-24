import sqlalchemy
from sqlalchemy.ext.declarative import as_declarative, declarative_base, declared_attr

# pylint: disable=no-member
# pylint: disable=no-self-argument

# SOURCE: full-stack-fastapi-postgresql
# @as_declarative()
# class Base:
#     id: Any
#     __name__: str
#     # Generate __tablename__ automatically
#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()


class CustomBase(object):
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


Base = declarative_base(cls=CustomBase)

metadata = Base.metadata
