from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy import JSON
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ultron8.api.db.u_sqlite.base_class import Base
from ultron8.api.db_models.ultronbase import UIDFieldMixin, ContentPackResourceMixin
from ultron8.consts import ResourceType

from ultron8.api.models.system.common import ResourceReference

PACK_SEPARATOR = "."


class RunnerTypeDB(UIDFieldMixin, Base):
    """Db Schema for RunnerTypeDB table."""

    RESOURCE_TYPE = ResourceType.RUNNER_TYPE
    UID_FIELDS = ["name"]

    __tablename__ = "runner_type"

    id = Column(Integer, primary_key=True, index=True)
    enabled = Column("enabled", Boolean)
    uid = Column("uid", String(255))
    runner_package = Column("runner_package", String(255))
    runner_module = Column("runner_module", String(255))
    runner_parameters = Column("runner_parameters", JSON)
    output_key = Column("output_key", String(255))
    output_schema = Column("output_schema", JSON)
    query_module = Column("query_module", String(255))

    def __init__(self, *args, **values):
        super(RunnerTypeDB, self).__init__(*args, **values)
        self.uid = self.get_uid()

    def __repr__(self):
        return "RunnerTypeDB<runner_package=%s,runner_module=%s>" % (
            self.runner_package,
            self.runner_module,
        )


MODELS = [RunnerTypeDB]
