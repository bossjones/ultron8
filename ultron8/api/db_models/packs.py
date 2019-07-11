from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ultron8.api.db.u_sqlite.base_class import Base
from ultron8.api.db_models.ultronbase import ContentPackResourceMixin, UIDFieldMixin
from ultron8.consts import ResourceType

PACKS_ACTIONS_ASSOCIATION = Table(
    "packs_actions",
    Base.metadata,
    Column("pack_id", Integer, ForeignKey("packs.id")),
    Column("action_id", Integer, ForeignKey("actions.id")),
)


class Packs(ContentPackResourceMixin, UIDFieldMixin, Base):
    """Db Schema for Packs table."""

    RESOURCE_TYPE = ResourceType.PACK
    UID_FIELDS = ["ref"]

    __tablename__ = "packs"

    id = Column("id", Integer, primary_key=True, index=True)
    ref = Column("ref", String(255), nullable=True)
    uid = Column("uid", String(255), nullable=True)
    name = Column("name", String(255), nullable=False)
    description = Column("description", String(255), nullable=False)
    keywords = Column("keywords", String(255))
    version = Column("version", String(255), nullable=False)
    python_versions = Column("python_versions", String(255))
    author = Column("author", String(255), nullable=False)
    email = Column("email", String(255))

    # contributors = me.ListField(field=me.StringField())
    contributors = Column("contributors", String(255))
    # files = me.ListField(field=me.StringField())
    files = Column("files", String(255))
    # path = Column(String(255), nullable=True)
    path = Column("path", String(255), nullable=True)
    dependencies = Column("dependencies", String(255), nullable=True)
    # dependencies = me.ListField(field=me.StringField())
    system = Column("system", String(255), nullable=True)
    # system = me.DictField()
    created_at = Column(DateTime(timezone=True), server_default=func.utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=func.utcnow())

    # Relationship: One To Many
    # actions = relationship("Action")
    # actions = relationship("Action", back_populates="packs", cascade="all, delete-orphan")
    # NOTE: Borrow this shit below
    # employees = relationship(
    #     "Person", back_populates="company", cascade="all, delete-orphan"
    # )

    # Inspired by: https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/
    # # and we added the actions property to Packs and configured the
    # packs_actions_association as the intermediary table.
    actions = relationship("Action", secondary=PACKS_ACTIONS_ASSOCIATION)

    def __init__(self, *args, **values):
        super(Packs, self).__init__(*args, **values)
        self.ref = self.get_reference().ref
        self.uid = self.get_uid()

    def __repr__(self):
        return "Packs(name=%s)" % (self.name)


if "__main__" == __name__:
    packs = Packs()

    print(packs)
