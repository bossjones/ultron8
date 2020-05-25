from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ultron8.api.db.u_sqlite.base_class import Base

if TYPE_CHECKING:
    from ultron8.api.db_models.user import User  # noqa: F401


class Item(Base):
    __tablename__ = "item"
    id = Column("id", Integer, primary_key=True, index=True)
    title = Column("title", String, index=True)
    description = Column("description", String, index=True)
    owner_id = Column("owner_id", Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="items")
