import datetime
from uuid import uuid4
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import String
from ultron8.api.db.u_sqlite.base_class import Base

from ultron8.api.db_models.types import ArrayType


class AccessToken(Base):
    __tablename__ = "access_token"
    id = Column("id", Integer, primary_key=True)
    created = Column("created", DateTime, default=datetime.datetime.utcnow)
    modified = Column("modified", DateTime, default=datetime.datetime.utcnow)
    app = Column(Integer, ForeignKey("app.id"))
    scopes = Column(ArrayType(String), default=[])
    access_token = Column(String(36), default=uuid4)
