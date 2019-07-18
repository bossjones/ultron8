from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String

from ultron8.api.db.u_sqlite.base_class import Base


class Guid(Base):
    __tablename__ = "guid_tracker"
    id = Column("id", String, primary_key=True)
    name = Column("name", String)
    expire = Column("expire", DateTime)


if "__main__" == __name__:
    guid = Guid()

    print(guid)
