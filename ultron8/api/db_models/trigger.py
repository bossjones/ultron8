from __future__ import absolute_import
import json
import hashlib

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

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

    ref = Column(String)
    name = Column(String)
    pack = relationship("Packs")
    payload_schema = Column(JSON)
    parameters_schema = Column(JSON)

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

    ref = Column(String)
    name = Column(String, nullable=False)
    pack = relationship("Packs", nullable=False)
    type = Column(String)
    parameters = Column(JSON)
    parameters = Column(Integer)

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


class TriggerInstanceDB(UIDFieldMixin, Base):
    """An instance or occurrence of a type of Trigger.
    Attribute:
        trigger: Reference to the Trigger object.
        payload (dict): payload specific to the occurrence.
        occurrence_time (datetime): time of occurrence of the trigger.
    """

    trigger = Column(String, index=True)
    payload = Column(JSON, index=True)
    occurrence_time = Column(JSON, index=True)
    occurrence_time = Column(DateTime(timezone=True), onupdate=func.utcnow())

    status = Column(String, index=True, nullable=False)


MODELS = [TriggerType, Trigger, TriggerInstanceDB]


if "__main__" == __name__:
    sensors = TriggerType()

    print(sensors)
