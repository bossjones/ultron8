import logging
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import JSON
from sqlalchemy import Boolean
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ultron8.api.db.u_sqlite.base_class import Base
from ultron8.api.db_models.ultronbase import UIDFieldMixin, ContentPackResourceMixin
from ultron8.consts import ResourceType

from ultron8.api.models.system.common import ResourceReference
import datetime
from sqlalchemy.ext.hybrid import hybrid_property

LOGGER = logging.getLogger(__name__)

# SOURCE: https://docs.sqlalchemy.org/en/13/dialects/sqlite.html
# NOTE: acceptable sqlite types
# from sqlalchemy.dialects.sqlite import \
#             BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, \
#             INTEGER, NUMERIC, JSON, SMALLINT, TEXT, TIME, TIMESTAMP, \
#             VARCHAR

# from ultron8.api.db.base import Base


# class Action(ContentPackResourceMixin, UIDFieldMixin, Base):
class Action(UIDFieldMixin, Base):
    """Db Schema for Action table."""

    RESOURCE_TYPE = ResourceType.ACTION
    UID_FIELDS = ["packs_name", "name"]

    __tablename__ = "actions"

    # __table_args__ = (UniqueConstraint('pack', 'name', name='_customer_location_uc'),
    # SOURCE: https://stackoverflow.com/questions/10059345/sqlalchemy-unique-across-multiple-columns
    # __table_args__ = (UniqueConstraint("pack", "name"),)

    id = Column(Integer, primary_key=True, index=True)
    # NOTE: New
    ref = Column("ref", String(255))
    uid = Column("uid", String(255))
    metadata_file = Column("metadata_file", String(255), nullable=True)
    name = Column("name", String(255))
    description = Column("description", String(255))
    runner_type = Column("runner_type", String(255))
    enabled = Column("enabled", Boolean)
    entry_point = Column("entry_point", String(255))
    parameters = Column("parameters", JSON)
    tags = Column("tags", JSON, nullable=True)
    created_at = Column("created_at", String)
    updated_at = Column("updated_at", String)
    packs_id = Column("packs_id", Integer, ForeignKey("packs.id"))

    def __init__(self, *args, packs_name=None, **values):
        super(Action, self).__init__(*args, **values)
        self.packs_name = packs_name
        # self._ref = self.get_reference().ref
        self.ref = "{}.{}".format(self.packs_name, self.name)
        self.uid = self.get_uid()
        # self.pack = self.pack
        self.created_at = str(datetime.datetime.utcnow())
        self.updated_at = str(datetime.datetime.utcnow())

    # def get_ref(self):
    #     return "{}.{}".format(self.pack.name, self.name)

    # @hybrid_property
    # def ref(self):
    #     return self.get_ref()

    # def get_packs_name(self):
    #     """
    #     Retrieve packs.name object for this model.

    #     :rtype: :class:`String`
    #     """
    #     # print("HELP: %s" % self.pack)
    #     # print("HELP: %s" % type(self.pack))
    #     # import pdb;pdb.set_trace()

    #     # FIXME: This is brittle AF
    #     if getattr(self, "packs_name", None):
    #         packs_name = self.pack.name
    #     else:
    #         packs_name = self.packs_name

    #     return packs_name

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
        return "Action<name=%s,ref=%s,runner_type=%s,entry_point=%s>" % (
            self.name,
            self.ref,
            self.runner_type,
            self.entry_point,
        )
