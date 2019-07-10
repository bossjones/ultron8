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

# from ultron8.api.db.base import Base


class Action(UIDFieldMixin, Base):
    """Db Schema for Action table."""

    RESOURCE_TYPE = ResourceType.ACTION
    UID_FIELDS = ["pack", "name"]

    __tablename__ = "action"

    id = Column(Integer, primary_key=True, index=True)
    # NOTE: New
    ref = Column("ref", String(255))
    uid = Column("uid", String(255))
    metadata_file = Column("metadata_file", String(255), nullable=True)
    packs_id = Column("packs_id", Integer, ForeignKey("packs.id"))
    pack = relationship("Packs")
    name = Column("name", String(255))
    runner_type = Column("runner_type", String(255))
    enabled = Column("enabled", String(255))
    entry_point = Column("entry_point", String(255))
    parameters = Column("parameters", String(255))
    tags = Column("tags", String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=func.utcnow())

    def __init__(self, *args, **values):
        self.ref = self.get_reference().ref
        self.uid = self.get_uid()


if "__main__" == __name__:
    action = Action()

    print(action)
