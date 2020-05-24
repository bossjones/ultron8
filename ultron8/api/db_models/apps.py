import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from ultron8.api.db.u_sqlite.base_class import Base
from ultron8.api.db_models.types import DateTime


class App(Base):
    __tablename__ = "app"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(254))
    created = Column("created", DateTime, default=datetime.datetime.utcnow)
    modified = Column("modified", DateTime, default=datetime.datetime.utcnow)
    client_id = Column("client_id", String(36), default=uuid4)
    client_secret = Column("client_secret", String(36), default=uuid4)

    access_tokens = relationship("AccessToken")
