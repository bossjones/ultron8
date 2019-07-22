from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import JSON
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ultron8.api.db.u_sqlite.base_class import Base
from ultron8.api.db_models.ultronbase import UIDFieldMixin, ContentPackResourceMixin
from ultron8.consts import ResourceType

from ultron8.api.models.system.common import ResourceReference

# from ultron8.api.db.base import Base


# class Action(ContentPackResourceMixin, UIDFieldMixin, Base):
class Action(UIDFieldMixin, Base):
    """Db Schema for Action table."""

    RESOURCE_TYPE = ResourceType.ACTION
    # UID_FIELDS = ["packs_name", "name"]
    UID_FIELDS = ["metadata_file", "name"]

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
    enabled = Column("enabled", String(255))
    entry_point = Column("entry_point", String(255))
    parameters = Column("parameters", JSON)
    tags = Column("tags", String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=func.utcnow())

    # packs_id = Column("packs_id", Integer, ForeignKey("packs.id"), nullable=True)
    # packs_name = Column("packs_name", Integer, ForeignKey("packs.name"), nullable=True)

    packs_id = Column("packs_id", Integer, ForeignKey("packs.id"))
    # packs_name = Column("packs_name", Integer, ForeignKey("packs.name"))

    # FIX: sqlalchemy Error creating backref on relationship
    # https://stackoverflow.com/questions/26693041/sqlalchemy-error-creating-backref-on-relationship
    # pack = relationship(
    #     "Packs",
    #     backref=backref("pack_actions", uselist=False),
    #     foreign_keys=[packs_id],
    #     # back_populates="actions",
    #     lazy=True
    # )
    # pack = relationship(
    #     "Packs",
    #     back_populates="actions"
    # )

    # pack = relationship("Packs", back_populates="actions", foreign_keys=[packs_id, packs_name])

    # pack = relationship("Packs")

    # def __init__(self, pack, *args, **values):
    def __init__(self, *args, **values):
        super(Action, self).__init__(*args, **values)
        self.ref = self.get_reference().ref
        self.uid = self.get_uid()
        # self.pack = self.pack

    def get_packs_name(self):
        """
        Retrieve packs.name object for this model.

        :rtype: :class:`String`
        """
        # FIXME: This is brittle AF
        if getattr(self, "packs_name", None):
            packs_name = self.pack.name
        else:
            packs_name = self.packs_name

        return packs_name

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
        return "Action<name=%s,ref=%s,runner_type=%s,entry_point=%s>" % (
            self.name,
            self.ref,
            self.runner_type,
            self.entry_point,
        )

    # def dump(self, _indent=0):
    #     return (
    #         "   " * _indent
    #         + repr(self)
    #         + "\n"
    #         + "".join([c.dump(_indent + 1) for c in self.children.values()])
    #     )


# smoke tests
if "__main__" == __name__:
    # Initial - Setup environment vars before testing anything
    import os
    from sqlalchemy import inspect

    # import better_exceptions; better_exceptions.hook()

    import sys

    from IPython.core.debugger import Tracer  # noqa
    from IPython.core import ultratb

    sys.excepthook = ultratb.FormattedTB(
        mode="Verbose", color_scheme="Linux", call_pdb=True, ostream=sys.__stdout__
    )

    os.environ["DEBUG"] = "1"
    os.environ["TESTING"] = "0"
    os.environ["BETTER_EXCEPTIONS"] = "1"

    # os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    # os.environ["TEST_DATABASE_URL"] = "sqlite:///:memory:"

    os.environ["DATABASE_URL"] = "sqlite:///test.db"
    os.environ["TEST_DATABASE_URL"] = "sqlite:///test.db"

    def debug_dump(obj):
        for attr in dir(obj):
            if hasattr(obj, attr):
                print("obj.%s = %s" % (attr, getattr(obj, attr)))

    import logging

    from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

    from ultron8.api.db.u_sqlite.session import db_session

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    max_tries = 60 * 5  # 5 minutes
    wait_seconds = 1

    @retry(
        stop=stop_after_attempt(max_tries),
        wait=wait_fixed(wait_seconds),
        before=before_log(logger, logging.INFO),
        after=after_log(logger, logging.WARN),
    )
    def init():
        try:
            # Try to create session to check if DB is awake
            # pylint: disable=no-member
            db_session.execute("SELECT 1")
        except Exception as e:
            logger.error(e)
            raise e

    # Get sqlalchemy classes/objects

    from ultron8.api.db.u_sqlite.init_db import init_db
    from ultron8.api.db.u_sqlite.session import db_session, engine, Session

    # make sure all SQL Alchemy models are imported before initializing DB
    # otherwise, SQL Alchemy might fail to initialize properly relationships
    # for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
    from ultron8.api.db.u_sqlite.base import Base

    import pandas as pd

    from ultron8.api.db_models.packs import Packs
    from ultron8.api.db_models.action import Action

    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # 2 - generate database schema
    Base.metadata.create_all(bind=engine)

    # 3 - create a new session
    session = Session()

    # Try initializing everything now
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")

    logger.info("Creating initial data")
    init_db(db_session)
    logger.info("Initial data created")

    ##########################################
    # packs
    ##########################################

    # p = Packs(name='linux', description='Generic Linux actions', keywords='linux', version='0.1.0', python_versions='3', author='Jarvis', email='info@theblacktonystark.com', contributors='bossjones', files='./tests/fixtures/simple/packs/linux', path="./tests/fixtures/simple/packs/linux", actions=[
    #     Action(name="check_loadavg", runner_type="remote-shell-script", description="Check CPU Load Average on a Host", enabled=True, entry_point="checks/check_loadavg.py", parameters='{"period": {"enum": ["1","5","15","all"], "type": "string", "description": "Time period for load avg: 1,5,15 minutes, or \'all\'", "default": "all", "position": 0}}')
    # ])

    # Create - packs
    pack_linux = Packs(
        name="linux",
        description="Generic Linux actions",
        keywords="linux",
        version="0.1.0",
        python_versions="3",
        author="Jarvis",
        email="info@theblacktonystark.com",
        contributors="bossjones",
        files="./tests/fixtures/simple/packs/linux",
        path="./tests/fixtures/simple/packs/linux",
        ref="linux",
    )

    print(pack_linux)

    action_check_loadavg = Action(
        name="check_loadavg",
        runner_type="remote-shell-script",
        description="Check CPU Load Average on a Host",
        enabled=True,
        entry_point="checks/check_loadavg.py",
        # parameters='{"period": {"enum": ["1","5","15","all"], "type": "string", "description": "Time period for load avg: 1,5,15 minutes, or \'all\'", "default": "all", "position": 0}}',
        parameters={
            "period": {
                "enum": ["1", "5", "15", "all"],
                "type": "string",
                "description": "Time period for load avg: 1,5,15 minutes, or 'all'",
                "default": "all",
                "position": 0,
            }
        },
        pack=pack_linux,
    )

    # print(action)
