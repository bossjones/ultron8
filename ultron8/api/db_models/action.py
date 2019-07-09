from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# from ultron8.api.db.base import Base
from ultron8.api.db.u_sqlite.base_class import Base
from ultron8.api.db_models.ultronbase import UIDFieldMixin
from ultron8.consts import ResourceType


class Action(UIDFieldMixin, Base):
    """Db Schema for Action table."""

    RESOURCE_TYPE = ResourceType.ACTION
    UID_FIELDS = ["pack", "name"]

    __tablename__ = "action"

    id = Column(Integer, primary_key=True, index=True)
    # NOTE: New
    ref = Column(String)
    uid = Column(String)
    metadata_file = Column(String, nullable=True)
    packs_id = Column(Integer, ForeignKey("packs.id"))
    pack = relationship("Packs")
    name = Column(String)
    runner_type = Column(String)
    enabled = Column(String)
    entry_point = Column(String)
    parameters = Column(String)
    tags = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=func.utcnow())

    def __init__(self, *args, **values):
        self.ref = self.get_reference().ref
        self.uid = self.get_uid()


if "__main__" == __name__:
    action = Action()

    print(action)
