from __future__ import absolute_import

import hashlib
import json

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import JSON
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ultron8.api.db.u_sqlite.base_class import Base
from ultron8.api.db_models.ultronbase import UIDFieldMixin, ContentPackResourceMixin
from ultron8.consts import ResourceType

from ultron8.api.models.system.common import ResourceReference


class TriggerTypeDB(UIDFieldMixin, Base):
    """
    Description of a specific kind/type of a trigger. The
       (pack, name) tuple is expected uniquely identify a trigger in
       the namespace of all triggers provided by a specific trigger_source.
    Attribute:
        name - Trigger type name.
        pack - Name of the content pack this trigger belongs to.
        trigger_source: Source that owns this trigger type.
        payload_info: Meta information of the expected payload.
    """

    RESOURCE_TYPE = ResourceType.TRIGGER_TYPE
    UID_FIELDS = ["packs_name", "name"]

    __tablename__ = "trigger_types"

    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String(255))
    ref = Column("ref", String(255))
    uid = Column("uid", String(255), nullable=True)
    pack = relationship("Packs")
    packs_id = Column("packs_id", Integer, ForeignKey("packs.id"))
    description = Column("description", String(255))
    payload_schema = Column("payload_schema", JSON)
    parameters_schema = Column("parameters_schema", JSON)

    packs_id = Column("packs_id", Integer, ForeignKey("packs.id"), nullable=True)
    packs_name = Column("packs_name", Integer, ForeignKey("packs.name"), nullable=True)
    # FIX: sqlalchemy Error creating backref on relationship
    # https://stackoverflow.com/questions/26693041/sqlalchemy-error-creating-backref-on-relationship
    pack = relationship(
        "Packs", backref=backref("pack_actions", uselist=False), foreign_keys=[packs_id]
    )

    def __init__(self, *args, **values):
        super(TriggerTypeDB, self).__init__(*args, **values)
        self.ref = self.get_reference().ref
        # pylint: disable=no-member
        self.uid = self.get_uid()

    def get_reference(self):
        """
        Retrieve referene object for this model.

        :rtype: :class:`ResourceReference`
        """
        if getattr(self, "ref", None):
            ref = ResourceReference.from_string_reference(ref=self.ref)
        else:
            ref = ResourceReference(pack=self.pack, name=self.name)

        return ref

    def __repr__(self):
        return "TriggerTypeDB<name=%s,ref=%s>" % (self.name, self.ref)


class TriggerDB(UIDFieldMixin, Base):
    """
    Basically events emitted by a sensor.

    Attribute:
        name - Trigger name.
        pack - Name of the content pack this trigger belongs to.
        type - Reference to the TriggerType object.
        parameters - Trigger parameters.
    """

    RESOURCE_TYPE = ResourceType.TRIGGER
    UID_FIELDS = ["packs_name", "name"]

    __tablename__ = "triggers"

    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String, nullable=False)
    ref = Column("ref", String(255))
    uid = Column("uid", String(255), nullable=True)
    type = Column("type", String(255))
    parameters = Column("parameters", JSON)
    ref_count = Column("ref_count", Integer)

    packs_id = Column("packs_id", Integer, ForeignKey("packs.id"), nullable=True)
    packs_name = Column("packs_name", Integer, ForeignKey("packs.name"), nullable=True)
    # FIX: sqlalchemy Error creating backref on relationship
    # https://stackoverflow.com/questions/26693041/sqlalchemy-error-creating-backref-on-relationship
    pack = relationship(
        "Packs",
        backref=backref("pack_triggers", uselist=False),
        foreign_keys=[packs_id],
    )

    def __init__(self, *args, **values):
        super(TriggerDB, self).__init__(*args, **values)
        self.ref = self.get_reference().ref
        self.uid = self.get_uid()

    def get_reference(self):
        """
        Retrieve referene object for this model.

        :rtype: :class:`ResourceReference`
        """
        if getattr(self, "ref", None):
            ref = ResourceReference.from_string_reference(ref=self.ref)
        else:
            ref = ResourceReference(pack=self.pack, name=self.name)

        return ref

    def get_uid(self):
        # Note: Trigger is uniquely identified using name + pack + parameters attributes
        # pylint: disable=no-member
        uid = super(TriggerDB, self).get_uid()

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

    def __repr__(self):
        return "TriggerDB<name=%s,ref=%s>" % (self.name, self.ref)


class TriggerInstanceDB(Base):
    """
    An instance or occurrence of a type of Trigger.

    Attribute:
        trigger: Reference to the Trigger object.
        payload (dict): payload specific to the occurrence.
        occurrence_time (datetime): time of occurrence of the trigger.
    """

    __tablename__ = "trigger_events"

    id = Column("id", Integer, primary_key=True, index=True)
    trigger = Column("trigger", String(255))
    payload = Column("payload", JSON)
    occurrence_time = Column(DateTime(timezone=True), onupdate=func.utcnow())
    status = Column("status", String(255), nullable=False)

    def __repr__(self):
        return "TriggerInstanceDB<trigger=%s,payload=%s>" % (self.trigger, self.payload)


MODELS = [TriggerTypeDB, TriggerDB, TriggerInstanceDB]


if "__main__" == __name__:
    trigger = TriggerTypeDB()

    print(trigger)
