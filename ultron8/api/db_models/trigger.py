from __future__ import absolute_import

import hashlib
import json

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ultron8.api.db.u_sqlite.base_class import Base
from ultron8.api.db_models.ultronbase import UIDFieldMixin
from ultron8.consts import ResourceType


class TriggerType(UIDFieldMixin, Base):
    """Description of a specific kind/type of a trigger. The
       (pack, name) tuple is expected uniquely identify a trigger in
       the namespace of all triggers provided by a specific trigger_source.
    Attribute:
        name - Trigger type name.
        pack - Name of the content pack this trigger belongs to.
        trigger_source: Source that owns this trigger type.
        payload_info: Meta information of the expected payload.
    """

    RESOURCE_TYPE = ResourceType.TRIGGER_TYPE
    UID_FIELDS = ["pack", "name"]

    __tablename__ = "trigger_types"

    id = Column("id", Integer, primary_key=True, index=True)
    ref = Column("ref", String(255))
    uid = Column("uid", String(255), nullable=True)
    name = Column("name", String(255))
    pack = relationship("Packs")
    packs_id = Column("packs_id", Integer, ForeignKey("packs.id"))
    description = Column("description", String(255))
    payload_schema = Column("payload_schema", String(255))
    parameters_schema = Column("parameters_schema", String(255))

    def __init__(self, *args, **values):
        self.ref = self.get_reference().ref
        # pylint: disable=no-member
        self.uid = self.get_uid()


class Trigger(UIDFieldMixin, Base):
    """
    Attribute:
        name - Trigger name.
        pack - Name of the content pack this trigger belongs to.
        type - Reference to the TriggerType object.
        parameters - Trigger parameters.
    """

    RESOURCE_TYPE = ResourceType.TRIGGER
    UID_FIELDS = ["pack", "name"]

    __tablename__ = "triggers"

    id = Column("id", Integer, primary_key=True, index=True)
    ref = Column("ref", String(255))
    uid = Column("uid", String(255), nullable=True)
    name = Column("name", String, nullable=False)
    pack = relationship("Packs")
    packs_id = Column("packs_id", Integer, ForeignKey("packs.id"))
    type = Column("type", String(255))
    parameters = Column("parameters", String(255))
    ref_count = Column("ref_count", Integer)

    def __init__(self, *args, **values):
        self.ref = self.get_reference().ref
        self.uid = self.get_uid()

    def get_uid(self):
        # Note: Trigger is uniquely identified using name + pack + parameters attributes
        # pylint: disable=no-member
        uid = super(Trigger, self).get_uid()

        # Note: We sort the resulting JSON object so that the same dictionary always results
        # in the same hash
        parameters = getattr(self, "parameters", {})
        parameters = json.dumps(parameters, sort_keys=True)
        parameters = hashlib.md5(parameters.encode()).hexdigest()

        uid = uid + self.UID_SEPARATOR + parameters
        return uid

    def has_valid_uid(self):
        parts = self.get_uid_parts()
        # Note: We add 1 for parameters field which is not part of self.UID_FIELDS
        return len(parts) == len(self.UID_FIELDS) + 1 + 1


class TriggerInstanceDB(Base):
    """An instance or occurrence of a type of Trigger.
    Attribute:
        trigger: Reference to the Trigger object.
        payload (dict): payload specific to the occurrence.
        occurrence_time (datetime): time of occurrence of the trigger.
    """

    __tablename__ = "trigger_instances"

    id = Column("id", Integer, primary_key=True, index=True)
    trigger = Column("trigger", String(255))
    payload = Column("payload", String(255))
    occurrence_time = Column(DateTime(timezone=True), onupdate=func.utcnow())

    status = Column("status", String(255), nullable=False)


MODELS = [TriggerType, Trigger, TriggerInstanceDB]


if "__main__" == __name__:
    trigger = TriggerType()

    print(trigger)
