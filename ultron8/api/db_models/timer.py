from __future__ import absolute_import


from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ultron8.api.db.u_sqlite.base_class import Base
from ultron8.api.db_models.ultronbase import UIDFieldMixin
from ultron8.consts import ResourceType


class TimerDB(UIDFieldMixin, Base):
    """
    Note: Right now timer is a meta model which is not persisted in the database (it's only used
    for RBAC purposes).

    Attribute:
        name: Timer name - maps to the URL path (e.g. st2/ or my/webhook/one).
    """

    RESOURCE_TYPE = ResourceType.TIMER
    UID_FIELDS = ["packs_name", "name"]

    name = Column("name", String(255))
    uid = Column("uid", String(255), nullable=True)
    pack = relationship("Packs")
    type = Column("type", String(255))
    parameters = Column("parameters", String(255))

    def __init__(self, *args, **values):
        super(TimerDB, self).__init__(*args, **values)
        self.uid = self.get_uid()


MODELS = [TimerDB]


if "__main__" == __name__:
    timer = TimerDB()

    print(timer)
