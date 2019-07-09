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

    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String)
    name = Column(String)
    ref = Column(String)
    packs_id = Column(Integer, ForeignKey("packs.id"))
    pack = relationship("Packs")
    artifact_uri = Column(String)
    poll_interval = Column(Integer)
    enabled = Column(Boolean)
    entry_point = Column(String)
    description = Column(String)
    trigger_types = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=func.utcnow())

    def __init__(self, *args, **values):
        self.ref = self.get_reference().ref
        self.uid = self.get_uid()


MODELS = [Sensors]


if "__main__" == __name__:
    sensors = Sensors()

    print(sensors)
