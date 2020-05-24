from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql import func

from ultron8.api.db.u_sqlite.base_class import Base
from ultron8.debugger import debug_dump_exclude

SENSORS_TRIGGER_TYPES_ASSOCIATION = Table(
    "sensors_trigger_types_association",
    Base.metadata,
    Column("sensors_id", Integer(), ForeignKey("sensors.id"), primary_key=True),
    Column(
        "trigger_types_id", Integer(), ForeignKey("trigger_types.id"), primary_key=True
    ),
)
