from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# from ultron8.api.db.base import Base
from ultron8.api.db.u_sqlite.base_class import Base


class Action(Base):
    """Db Schema for Action table."""

    __tablename__ = "action"
    id = Column(Integer, primary_key=True, index=True)
    packs_id = Column(Integer, ForeignKey("packs.id"))
    pack = relationship("Packs")
    name = Column(String, index=True)
    runner_type = Column(String, index=True)
    enabled = Column(String, index=True)
    entry_point = Column(String, index=True)
    parameters = Column(String, index=True)
    tags = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=func.utcnow())


if "__main__" == __name__:
    action = Action()

    print(action)
