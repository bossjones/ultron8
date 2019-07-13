from sqlalchemy import Boolean
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

"""
class_name: "FileWatchSensor"
enabled: true
entry_point: "file_watch_sensor.py"
description: "Sensor which monitors files for new lines"
trigger_types:
  -
    name: "file_watch.line"
    pack: "linux"
    description: "Trigger which indicates a new line has been detected"
    # This sensor can be supplied a path to a file to tail via a rule.
    parameters_schema:
      type: "object"
      properties:
        file_path:
          description: "Path to the file to monitor"
          type: "string"
          required: true
      additionalProperties: false
    # This is the schema of the trigger payload the sensor generates
    payload_schema:
      type: "object"
      properties:
        file_path:
          type: "string"
        file_name:
          type: "string"
        line:
          type: "string"
"""

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
    UID_FIELDS = ["packs_name", "name"]

    __tablename__ = "sensors"

    id = Column("id", Integer, primary_key=True, index=True)
    # class_name = Column("class_name", String(255))
    name = Column("class_name", String(255))
    ref = Column("ref", String(255))
    uid = Column("uid", String(255), nullable=True)
    artifact_uri = Column("artifact_uri", String(255))
    poll_interval = Column("poll_interval", Integer)
    enabled = Column("enabled", Boolean)
    entry_point = Column("entry_point", String(255))
    description = Column("description", String(255))
    trigger_types = Column("trigger_types", JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=func.utcnow())

    packs_id = Column("packs_id", Integer, ForeignKey("packs.id"), nullable=True)
    packs_name = Column("packs_name", Integer, ForeignKey("packs.name"), nullable=True)
    # FIX: sqlalchemy Error creating backref on relationship
    # https://stackoverflow.com/questions/26693041/sqlalchemy-error-creating-backref-on-relationship
    pack = relationship(
        "Packs", backref=backref("pack_sensors", uselist=False), foreign_keys=[packs_id]
    )

    def __init__(self, *args, **values):
        super(Sensors, self).__init__(*args, **values)
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

    def __repr__(self):
        return "Sensor<name=%s,ref=%s,trigger_types=%s,entry_point=%s>" % (
            self.name,
            self.ref,
            self.trigger_types,
            self.entry_point,
        )
#######################################################################################################

MODELS = [Sensors]


# smoke-tests
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

    # action_check_loadavg = Action(
    #     name="check_loadavg",
    #     runner_type="remote-shell-script",
    #     description="Check CPU Load Average on a Host",
    #     enabled=True,
    #     entry_point="checks/check_loadavg.py",
    #     parameters='{"period": {"enum": ["1","5","15","all"], "type": "string", "description": "Time period for load avg: 1,5,15 minutes, or \'all\'", "default": "all", "position": 0}}',
    #     pack=pack_linux,
    # )

    sensors = Sensors(
        name="FileWatchSensor",
        enabled=True,
        entry_point="file_watch_sensor.py",
        description="Sensor which monitors files for new lines",
        trigger_types=[
            {
                "name": "file_watch.line",
                "pack": "linux",
                "description": "Trigger which indicates a new line has been detected",
                "parameters_schema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "description": "Path to the file to monitor",
                            "type": "string",
                            "required": True
                        }
                    },
                    "additionalProperties": False
                },
                "payload_schema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string"
                        },
                        "file_name": {
                            "type": "string"
                        },
                        "line": {
                            "type": "string"
                        }
                    }
                }
            }
        ],
        pack=pack_linux
    )

    print(sensors)
