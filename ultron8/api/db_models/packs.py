from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ultron8.api.db.u_sqlite.base_class import Base


class Packs(Base):
    """Db Schema for Packs table."""

    __tablename__ = "packs"
    id = Column(Integer, primary_key=True, index=True)
    ref = Column(String, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    keywords = Column(String, index=True)
    version = Column(String, index=True)
    python_versions = Column(String, index=True)
    author = Column(String, index=True)
    email = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=func.utcnow())


if "__main__" == __name__:
    packs = Packs()

    print(packs)
