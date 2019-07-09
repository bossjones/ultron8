from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ultron8.api.db.u_sqlite.base_class import Base
from ultron8.api.db_models.ultronbase import UIDFieldMixin
from ultron8.consts import ResourceType


class Packs(UIDFieldMixin, Base):
    """Db Schema for Packs table."""

    RESOURCE_TYPE = ResourceType.PACK
    UID_FIELDS = ["ref"]

    __tablename__ = "packs"

    id = Column(Integer, primary_key=True, index=True)
    ref = Column(String)
    name = Column(String)
    description = Column(String)
    keywords = Column(String)
    version = Column(String)
    python_versions = Column(String)
    author = Column(String)
    email = Column(String)

    # contributors = me.ListField(field=me.StringField())
    # files = me.ListField(field=me.StringField())
    # path = Column(String, nullable=True)
    # dependencies = me.ListField(field=me.StringField())
    # system = me.DictField()
    created_at = Column(DateTime(timezone=True), server_default=func.utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=func.utcnow())

    def __init__(self, *args, **values):
        self.ref = self.get_reference().ref
        self.uid = self.get_uid()


if "__main__" == __name__:
    packs = Packs()

    print(packs)
