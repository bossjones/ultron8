from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ultron8.api.db.u_sqlite.base_class import Base


class Sensors(Base):
    """Db Schema for Sensors table."""

    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String, index=True)
    enabled = Column(Boolean, index=True)
    entry_point = Column(String, index=True)
    description = Column(String, index=True)
    trigger_types = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=func.utcnow())


if "__main__" == __name__:
    sensors = Sensors()

    print(sensors)
