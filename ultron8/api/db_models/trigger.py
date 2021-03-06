from __future__ import absolute_import

import datetime
import hashlib
import json

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, orm
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql import func

from ultron8.api.db.u_sqlite.base_class import Base
from ultron8.api.db_models.sensors_trigger_types_association import (
    SENSORS_TRIGGER_TYPES_ASSOCIATION,
)
from ultron8.api.db_models.ultronbase import ContentPackResourceMixin, UIDFieldMixin
from ultron8.api.models.system.common import ResourceReference
from ultron8.consts import ResourceType

# http://blog.benjamin-encz.de/post/sqlite-one-to-many-json1-extension/


class TriggerTagsDB(Base):
    """Database model to support Trigger tags.

    Arguments:
        Base {[type]} -- SqlAlchemy Base model
    """

    __tablename__ = "trigger_tags"

    id = Column("id", Integer, primary_key=True, index=True)
    trigger_type_id = Column(
        "trigger_type_id", Integer, ForeignKey("trigger_types.id"), nullable=True
    )
    tag = Column("tag", String, nullable=True)
    trigger_name = Column("trigger_name", String, nullable=True)


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

    # /Users/malcolm/.virtualenvs/ultron8-cznMaMZB/lib/python3.6/site-packages/sqlalchemy/sql/crud.py:799: SAWarning: Column 'trigger_types.id' is marked as a member of the primary key for table 'trigger_types', but has no Python-side or server-side default generator indicated, nor does it indicate 'autoincrement=True' or 'nullable=True', and no explicit value is passed.  Primary key columns typically may not store NULL. Note that as of SQLAlchemy 1.1, 'autoincrement=True' must be indicated explicitly for composite (e.g. multicolumn) primary keys if AUTO_INCREMENT/SERIAL/IDENTITY behavior is expected for one of the columns in the primary key. CREATE TABLE statements are impacted by this change as well on most backends.
    # util.warn(msg)

    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String(255))
    ref = Column("ref", String(255))
    uid = Column("uid", String(255), nullable=True)
    description = Column("description", String(255))
    # payload_schema = Column("payload_schema", String(255))
    # parameters_schema = Column("parameters_schema", String(255))
    payload_schema = Column("payload_schema", JSON)
    parameters_schema = Column("parameters_schema", JSON)
    packs_id = Column("packs_id", Integer, ForeignKey("packs.id"), nullable=True)

    # Path to the metadata file relative to the pack directory.
    metadata_file = Column("metadata_file", String(255))
    tags = relationship("TriggerTagsDB", backref=backref("trigger", lazy="joined"))

    #################################################
    # ONE-TO-MANY - https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html
    #################################################
    # NOTE: trigger_types can be a child to sensors
    ########################
    # sensors_id = Column(Integer, ForeignKey("sensors.id"))
    # sensors = relationship(
    #     "ultron8.api.db_models.sensors.Sensors",
    #     foreign_keys="ultron8.api.db_models.trigger.TriggerTypeDB.sensors_id",
    #     back_populates="trigger_types",
    # )

    sensors = relationship(
        "ultron8.api.db_models.sensors.Sensors",
        secondary=SENSORS_TRIGGER_TYPES_ASSOCIATION,
        back_populates="trigger_types",
    )

    def __init__(self, *args, packs_name=None, **values):
        super(TriggerTypeDB, self).__init__(*args, **values)
        self.packs_name = packs_name
        # self.ref = self.get_reference().ref
        self.ref = "{}.{}".format(self.packs_name, self.name)
        # pylint: disable=no-member
        self.uid = self.get_uid()

    # @property
    # def args(self):
    #     return json.loads(self.arguments)

    # @args.setter
    # def args(self, value):
    #     self.arguments = json.dumps(value)

    # @property
    # def kwargs(self):
    #     return json.loads(self.keyword_arguments)

    # @kwargs.setter
    # def kwargs(self, kwargs_):
    #     self.keyword_arguments = json.dumps(kwargs_)

    # def get_reference(self):
    #     """
    #     Retrieve referene object for this model.

    #     :rtype: :class:`ResourceReference`
    #     """
    #     if getattr(self, "ref", None):
    #         ref = ResourceReference.from_string_reference(ref=self.ref)
    #     else:
    #         ref = ResourceReference(pack=self.pack, name=self.name)

    #     return ref

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
    description = Column("description", String, nullable=False)
    ref = Column("ref", String(255))
    uid = Column("uid", String(255), nullable=True)
    type = Column("type", String(255))
    parameters = Column("parameters", JSON)
    ref_count = Column("ref_count", Integer, default=0)
    packs_id = Column("packs_id", Integer, ForeignKey("packs.id"), nullable=True)
    # packs_name = Column("packs_name", Integer, ForeignKey("packs.name"), nullable=True)
    # FIX: sqlalchemy Error creating backref on relationship
    # https://stackoverflow.com/questions/26693041/sqlalchemy-error-creating-backref-on-relationship
    # pack = relationship(
    #     "Packs",
    #     backref=backref("pack_triggers", uselist=False),
    #     foreign_keys=[packs_id],
    # )

    def __init__(self, *args, packs_name=None, **values):
        super(TriggerDB, self).__init__(*args, **values)
        self.packs_name = packs_name
        # self._ref = self.get_reference().ref
        self.ref = "{}.{}".format(self.packs_name, self.name)
        self.uid = self.get_uid()

    # def get_reference(self):
    #     """
    #     Retrieve referene object for this model.

    #     :rtype: :class:`ResourceReference`
    #     """
    #     if getattr(self, "ref", None):
    #         ref = ResourceReference.from_string_reference(ref=self.ref)
    #     else:
    #         ref = ResourceReference(pack=self.pack, name=self.name)

    #     return ref

    # SOURCE: https://docs.sqlalchemy.org/en/13/orm/constructors.html
    # EXAMPLE: https://github.com/haobin12358/Weidian/blob/6c1b0fd54b1ed964f4b22a356a2a66cab9d91851/WeiDian/models/model.py
    @orm.reconstructor
    def get_uid(self) -> str:
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

    # SOURCE: https://docs.sqlalchemy.org/en/13/orm/constructors.html
    # EXAMPLE: https://github.com/haobin12358/Weidian/blob/6c1b0fd54b1ed964f4b22a356a2a66cab9d91851/WeiDian/models/model.py
    @orm.reconstructor
    def has_valid_uid(self) -> bool:
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
    # occurrence_time = Column(DateTime(timezone=True), onupdate=func.utcnow())
    occurrence_time = Column("occurrence_time", String)
    status = Column("status", String(255), nullable=False)

    def __init__(self, *args, **values):
        super(TriggerInstanceDB, self).__init__(*args, **values)
        self.occurrence_time = str(datetime.datetime.utcnow())

    def __repr__(self):
        return (
            "TriggerInstanceDB<trigger=%s,payload=%s,status=%s,occurrence_time=%s>"
            % (self.trigger, self.payload, self.status, self.occurrence_time)
        )


MODELS = [TriggerTypeDB, TriggerDB, TriggerInstanceDB]


if "__main__" == __name__:
    trigger = TriggerTypeDB()

    print(trigger)
