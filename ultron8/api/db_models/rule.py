from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ultron8.api.db.u_sqlite.base_class import Base


class Rules(Base):
    """Db Schema for Rules table."""

    __tablename__ = "rules"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    pack = Column(String, index=True)
    description = Column(String, index=True)
    enabled = Column(Boolean, index=True)
    trigger = Column(String, index=True)
    action = Column(String, index=True)
    ref = Column(String, index=True)
    type = Column(String, index=True)
    criteria = Column(String, index=True)
    context = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=func.utcnow())


if "__main__" == __name__:
    rules = Rules()

    print(rules)
