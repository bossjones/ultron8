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
from sqlalchemy import Table

from ultron8.api.db.u_sqlite.base_class import Base
from ultron8.api.db_models.ultronbase import UIDFieldMixin, ContentPackResourceMixin
from ultron8.consts import ResourceType
import datetime

from ultron8.api.models.system.common import ResourceReference

from ultron8.api.db_models.trigger import TriggerTypeDB

from sqlalchemy import and_
from ultron8.debugger import debug_dump_exclude

# assoc_table = db.Table('association',
#    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id')),
#    db.Column('cocktail_id', db.Integer, db.ForeignKey('cocktails.id'))
# )


# SENSORS_TRIGGER_TYPES_ASSOCIATION = Table(
#     "sensors_trigger_types_association",
#     Base.metadata,
#     Column("sensors_id", Integer, ForeignKey("sensors.id"), primary_key=True),
#     Column(
#         "trigger_types_id", Integer, ForeignKey("trigger_types.id", primary_key=True)
#     ),
#     Column(
#         "packs_id",
#         Integer,
#         ForeignKey("packs.id"),
#         primary_key=True,
#     ),
# )

SENSORS_TRIGGER_TYPES_ASSOCIATION = Table(
    "sensors_trigger_types_association",
    Base.metadata,
    Column(
        "sensors_packs_id", Integer(), ForeignKey("sensors.packs_id"), primary_key=True
    ),
    Column(
        "trigger_types_packs_id",
        Integer(),
        ForeignKey("trigger_types.packs_id"),
        primary_key=True,
    ),
)

# class Association(Base):
#     __tablename__ = 'association'
#     left_id = Column(Integer, ForeignKey('left.id'), primary_key=True)
#     right_id = Column(Integer, ForeignKey('right.id'), primary_key=True)
#     extra_data = Column(String(50))
#     child = relationship("Child", back_populates="parents")
#     parent = relationship("Parent", back_populates="children")

# NOTE: How to three-way many-to-many relationship in flask-sqlalchemy
# SOURCE: https://stackoverflow.com/questions/23035662/how-to-three-way-many-to-many-relationship-in-flask-sqlalchemy


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
    class_name = Column("class_name", String(255))
    ref = Column("ref", String(255))
    uid = Column("uid", String(255), nullable=True)
    artifact_uri = Column("artifact_uri", String(255))
    poll_interval = Column("poll_interval", Integer)
    enabled = Column("enabled", Boolean)
    entry_point = Column("entry_point", String(255))
    description = Column("description", String(255))
    # trigger_types = Column("trigger_types", JSON)
    # trigger_types_id = Column(
    #     "trigger_types_id", Integer, ForeignKey("trigger_types.id"), nullable=True
    # )

    created_at = Column("created_at", String)
    updated_at = Column("updated_at", String)
    packs_id = Column("packs_id", Integer, ForeignKey("packs.id"), nullable=True)
    # DISABLED: # trigger_types_id = Column(
    # DISABLED: #     "trigger_types_id", Integer, ForeignKey("trigger_types.id"), primary_key=True
    # DISABLED: # )
    # DISABLED: # triggers_types_packs_id = Column(
    # DISABLED: #     "triggers_types_packs_id",
    # DISABLED: #     Integer,
    # DISABLED: #     ForeignKey("trigger_types.packs_id"),
    # DISABLED: #     primary_key=True
    # DISABLED: # )
    # triggers_types_packs_id = Column("triggers_types_packs_id", Integer)
    # triggers_types_packs_id = Column("packs_id", Integer, ForeignKey("packs.id"), primary_key=True)
    # triggers_types_packs_id = Column(Integer, ForeignKey("triggers_types.id"), nullable=False)

    # trigger_types = relationship("TriggerTypeDB", backref=backref("sensor_trigger_types", lazy="joined"))
    # trigger_types = relationship("TriggerTypeDB", backref=backref("sensor_trigger_types", lazy="joined"))
    # trigger_types = relationship(
    #     "TriggerTypeDB",
    #     secondary=SENSORS_TRIGGER_TYPES_ASSOCIATION,
    #     backref=backref("sensor_trigger_types", lazy="dynamic")
    # )
    # trigger_types = relationship(
    #     "TriggerTypeDB",
    #     secondary=SENSORS_TRIGGER_TYPES_ASSOCIATION,
    #     backref=backref("sensor_trigger_types", lazy="joined"),
    #     foreign_keys=[packs_id]
    # )
    # trigger_types = relationship(
    #     "TriggerTypeDB",
    #     secondary=SENSORS_TRIGGER_TYPES_ASSOCIATION,
    #     backref=backref("sensor_trigger_types", lazy="joined")
    #     # foreign_keys=[triggers_types_packs_id]
    # )

    # FIXME: Recent attempts 8/9/2019
    # trigger_types = relationship(
    #     "TriggerTypeDB",
    #     secondary=SENSORS_TRIGGER_TYPES_ASSOCIATION,
    #     backref=backref("sensor_trigger_types", lazy="joined"),
    # )
    # trigger_types = relationship(
    #     "TriggerTypeDB", lazy="joined", cascade="all, delete"
    # )
    # trigger_types = relationship(
    #     "TriggerTypeDB", backref="sensors"
    # )

    # <><><><><><><><><><><><><><><><><><><>
    # Sensor = LEFT side of join
    # TriggerTypeDB = Right side of join
    # <><><><><><><><><><><><><><><><><><><>
    # relationship() using explicit foreign_keys, remote_side
    # HOW TO UNDERSTAND THIS: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-viii-followers
    trigger_types = relationship(
        # NOTE: is the right side entity of the relationship (the left side entity is the Sensor class).
        "TriggerTypeDB",
        # NOTE: Configures the association table that is used for this relationship, which I defined right above this class.
        secondary=SENSORS_TRIGGER_TYPES_ASSOCIATION,
        # NOTE: indicates the condition that links the left side entity (the sensor) with the association table. The join condition for the left side of the relationship is the user ID matching the sensors_packs_id field of the association table. The SENSORS_TRIGGER_TYPES_ASSOCIATION.c.sensors_packs_id expression references the sensors_packs_id column of the association table.
        primaryjoin=(
            SENSORS_TRIGGER_TYPES_ASSOCIATION.c.trigger_types_packs_id == packs_id
        ),
        # NOTE: indicates the condition that links the right side entity (the trigger_type) with the association table. This condition is similar to the one for primaryjoin, with the only difference that now I'm using sensors_packs_id, which is the other foreign key in the association table.
        secondaryjoin=(
            SENSORS_TRIGGER_TYPES_ASSOCIATION.c.sensors_packs_id == packs_id
        ),
        # NOTE: defines how this relationship will be accessed from the right side entity. From the left side, the relationship is named trigger_types, so from the right side I am going to use the name sensors to represent all the left side sensors that are linked to the trigger types in the right side. The additional lazy argument indicates the execution mode for this query. A mode of dynamic sets up the query to not run until specifically requested, which is also how I set up the posts one-to-many relationship.
        backref=backref("sensors", lazy="dynamic"),
        # backref=backref("sensors"),
        # foreign_keys=[packs_id],
        # foreign_keys=[packs_id],
        # foreign_keys=[SENSORS_TRIGGER_TYPES_ASSOCIATION.c.trigger_types_packs_id,
        # SENSORS_TRIGGER_TYPES_ASSOCIATION.c.sensors_packs_id],
        # NOTE: is similar to the parameter of the same name in the backref, but this one applies to the left side query instead of the right side.
        lazy="dynamic",
    )

    # # SOURCE: https://stackoverflow.com/questions/28503656/attributeerror-list-object-has-no-attribute-sa-instance-state/28503775#28503775
    # # is_bestfriend = db.relationship( 'Users', uselist=False, remote_side=[id], post_update=True)
    # trigger_types = relationship('TriggerTypeDB', #defining the relationship, Users is left side entity
    #     secondary = SENSORS_TRIGGER_TYPES_ASSOCIATION, #indecates association table
    #     primaryjoin = (SENSORS_TRIGGER_TYPES_ASSOCIATION.c.triggers_types_packs_id == packs_id), #condition linking the left side entity
    #     # secondaryjoin = (SENSORS_TRIGGER_TYPES_ASSOCIATION.c.friend_id == id),#cond if link right.s ent. with assoc table
    #     backref = backref('sensors_trigger_types_association', lazy = 'dynamic'),#how accessed from right
    #     lazy = 'dynamic'
    # )

    # trigger_types = relationship("TriggerTypeDB", backref=backref("sensor_trigger_types", lazy="joined"), foreign_keys=[triggers_types_packs_id])

    # trigger_types = relationship(
    #     "TriggerTypeDB", cascade="all, delete-orphan", backref="trigger_type"
    # )

    # Column(
    #     "trigger_types_id", Integer, ForeignKey("trigger_types.id")
    # ),
    # Column(
    #     "triggers_types_packs_id", Integer, ForeignKey("trigger_types.packs_id")
    # ),

    # # ---
    # # class_name: "SampleSensor"
    # # entry_point: "sample_sensor.py"
    # # description: "Sample sensor that emits triggers."
    # # trigger_types:
    # #   -
    # #     name: "event"
    # #     description: "An example trigger."
    # #     payload_schema:
    # #       type: "object"
    # #       properties:
    # #         executed_at:
    # #           type: "string"
    # #           format: "date-time"
    # #           default: "2014-07-30 05:04:24.578325"

    def __init__(self, *args, packs_name=None, **values):
        super(Sensors, self).__init__(*args, **values)
        self.packs_name = packs_name
        self.ref = "{}.{}".format(self.packs_name, self.class_name)
        self.uid = self.get_uid()
        self.created_at = str(datetime.datetime.utcnow())
        self.updated_at = str(datetime.datetime.utcnow())
        # self.triggers_types_packs_id = self.packs_id

    def get_trigger_types(self):
        """ Return list of Trigger Types associated with this Sensor. """
        # trigger_types = TriggerTypeDB.query.join(Sensors.packs_id == self.packs_id).all()
        #
        return self.trigger_types.filter(
            SENSORS_TRIGGER_TYPES_ASSOCIATION.c.trigger_types_packs_id == self.packs_id
        ).all()

    # def add_or_update_pattern_score(self, account_type, field, pattern, score):
    #     db_pattern_score = self.get_account_pattern_audit_score(account_type, field, pattern)
    #     if db_pattern_score is not None:
    #         db_pattern_score.score = score
    #     else:
    #         db_pattern_score = AccountPatternAuditScore(account_type=account_type,
    #                                                     account_field=field,
    #                                                     account_pattern=pattern,
    #                                                     score=score)

    #         self.account_pattern_scores.append(db_pattern_score)

    # def get_account_pattern_audit_score(self, account_type, field, pattern):
    #     for db_pattern_score in self.account_pattern_scores:
    #         if db_pattern_score.account_field == field and \
    #                 db_pattern_score.account_pattern == pattern and db_pattern_score.account_type == account_type:
    #             return db_pattern_score

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
        return (
            "Sensor<class_name=%s,ref=%s,uid=%s,artifact_uri=%s,poll_interval=%s,enabled=%s,entry_point=%s>"
            % (
                self.class_name,
                self.ref,
                self.uid,
                self.artifact_uri,
                self.poll_interval,
                self.enabled,
                self.entry_point,
            )
        )


#######################################################################################################

MODELS = [Sensors]


# # smoke-tests
# if "__main__" == __name__:
#     # Initial - Setup environment vars before testing anything
#     import os
#     from sqlalchemy import inspect

#     # import better_exceptions; better_exceptions.hook()

#     import sys

#     from IPython.core.debugger import Tracer  # noqa
#     from IPython.core import ultratb

#     sys.excepthook = ultratb.FormattedTB(
#         mode="Verbose", color_scheme="Linux", call_pdb=True, ostream=sys.__stdout__
#     )

#     os.environ["DEBUG"] = "1"
#     os.environ["TESTING"] = "0"
#     os.environ["BETTER_EXCEPTIONS"] = "1"

#     # os.environ["DATABASE_URL"] = "sqlite:///:memory:"
#     # os.environ["TEST_DATABASE_URL"] = "sqlite:///:memory:"

#     os.environ["DATABASE_URL"] = "sqlite:///test.db"
#     os.environ["TEST_DATABASE_URL"] = "sqlite:///test.db"

#     def debug_dump(obj):
#         for attr in dir(obj):
#             if hasattr(obj, attr):
#                 print("obj.%s = %s" % (attr, getattr(obj, attr)))

#     import logging

#     from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

#     from ultron8.api.db.u_sqlite.session import db_session

#     logging.basicConfig(level=logging.INFO)
#     logger = logging.getLogger(__name__)

#     max_tries = 60 * 5  # 5 minutes
#     wait_seconds = 1

#     @retry(
#         stop=stop_after_attempt(max_tries),
#         wait=wait_fixed(wait_seconds),
#         before=before_log(logger, logging.INFO),
#         after=after_log(logger, logging.WARN),
#     )
#     def init():
#         try:
#             # Try to create session to check if DB is awake
#             # pylint: disable=no-member
#             db_session.execute("SELECT 1")
#         except Exception as e:
#             logger.error(e)
#             raise e

#     # Get sqlalchemy classes/objects

#     from ultron8.api.db.u_sqlite.init_db import init_db
#     from ultron8.api.db.u_sqlite.session import db_session, engine, Session

#     # make sure all SQL Alchemy models are imported before initializing DB
#     # otherwise, SQL Alchemy might fail to initialize properly relationships
#     # for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
#     from ultron8.api.db.u_sqlite.base import Base

#     import pandas as pd

#     from ultron8.api.db_models.packs import Packs
#     from ultron8.api.db_models.action import Action

#     # Tables should be created with Alembic migrations
#     # But if you don't want to use migrations, create
#     # the tables un-commenting the next line
#     # 2 - generate database schema
#     Base.metadata.create_all(bind=engine)

#     # 3 - create a new session
#     session = Session()

#     # Try initializing everything now
#     logger.info("Initializing service")
#     init()
#     logger.info("Service finished initializing")

#     logger.info("Creating initial data")
#     init_db(db_session)
#     logger.info("Initial data created")

#     ##########################################
#     # packs
#     ##########################################

#     # Create - packs
#     pack_linux = Packs(
#         name="linux",
#         description="Generic Linux actions",
#         keywords="linux",
#         version="0.1.0",
#         python_versions="3",
#         author="Jarvis",
#         email="info@theblacktonystark.com",
#         contributors="bossjones",
#         files="./tests/fixtures/simple/packs/linux",
#         path="./tests/fixtures/simple/packs/linux",
#         ref="linux",
#     )

#     print(pack_linux)

#     # action_check_loadavg = Action(
#     #     name="check_loadavg",
#     #     runner_type="remote-shell-script",
#     #     description="Check CPU Load Average on a Host",
#     #     enabled=True,
#     #     entry_point="checks/check_loadavg.py",
#     #     parameters='{"period": {"enum": ["1","5","15","all"], "type": "string", "description": "Time period for load avg: 1,5,15 minutes, or \'all\'", "default": "all", "position": 0}}',
#     #     pack=pack_linux,
#     # )

#     sensors = Sensors(
#         name="FileWatchSensor",
#         enabled=True,
#         entry_point="file_watch_sensor.py",
#         description="Sensor which monitors files for new lines",
#         trigger_types=[
#             {
#                 "name": "file_watch.line",
#                 "pack": "linux",
#                 "description": "Trigger which indicates a new line has been detected",
#                 "parameters_schema": {
#                     "type": "object",
#                     "properties": {
#                         "file_path": {
#                             "description": "Path to the file to monitor",
#                             "type": "string",
#                             "required": True,
#                         }
#                     },
#                     "additionalProperties": False,
#                 },
#                 "payload_schema": {
#                     "type": "object",
#                     "properties": {
#                         "file_path": {"type": "string"},
#                         "file_name": {"type": "string"},
#                         "line": {"type": "string"},
#                     },
#                 },
#             }
#         ],
#         pack=pack_linux,
#     )

#     print(sensors)
