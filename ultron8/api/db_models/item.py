from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from ultron8.api.db.u_sqlite.base_class import Base


class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="items")
