from sqlalchemy import Boolean
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


class Sensors(UIDFieldMixin, Base):
    """
    Description of a specific type of a sensor (think of it as a sensor
    template).

    Attribute:
        pack - Name of the content pack this sensor belongs to.
        artifact_uri - URI to the artifact file.
        entry_point - Full path to the sensor entry point (e.g. module.foo.ClassSensor).
        trigger_type - A list of references to the TriggerTypeDB objects exposed by this sensor.
        poll_interval - Poll interval for this sensor.
    """

    RESOURCE_TYPE = ResourceType.SENSOR_TYPE
    UID_FIELDS = ["pack", "name"]

    __tablename__ = "sensors"

    id = Column("id", Integer, primary_key=True, index=True)
    class_name = Column("class_name", String(255))
    name = Column("name", String(255))
    ref = Column("ref", String(255))
    uid = Column("uid", String(255), nullable=True)
    # packs_id = Column("packs_id", Integer, ForeignKey("packs.id"))
    pack = relationship("Packs")
    artifact_uri = Column("artifact_uri", String(255))
    poll_interval = Column("poll_interval", Integer)
    enabled = Column("enabled", Boolean)
    entry_point = Column("entry_point", String(255))
    description = Column("description", String(255))
    trigger_types = Column("trigger_types", String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=func.utcnow())

    def __init__(self, *args, **values):
        self.ref = self.get_reference().ref
        self.uid = self.get_uid()


MODELS = [Sensors]


if "__main__" == __name__:
    sensors = Sensors()

    print(sensors)
