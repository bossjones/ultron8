from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ultron8.api.db.u_sqlite.base_class import Base


class Sensors(Base):
    """Db Schema for Sensors table."""

    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String)
    ref = Column(String)
    packs_id = Column(Integer, ForeignKey("packs.id"))
    pack = relationship("Packs")
    enabled = Column(Boolean)
    entry_point = Column(String)
    description = Column(String)
    trigger_types = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=func.utcnow())


if "__main__" == __name__:
    sensors = Sensors()

    print(sensors)
