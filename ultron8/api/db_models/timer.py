from __future__ import absolute_import

import hashlib
import json

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
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
    UID_FIELDS = ["pack", "name"]

    name = Column(String)
    pack = relationship("Packs")
    type = Column(String)
    parameters = Column(JSON)

    def __init__(self, *args, **values):
        super(TimerDB, self).__init__(*args, **values)
        self.uid = self.get_uid()


MODELS = [TimerDB]


if "__main__" == __name__:
    timer = TimerDB()

    print(timer)
