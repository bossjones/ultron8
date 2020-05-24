import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    and_,
    orm,
)
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql import func

from ultron8.api.db.u_sqlite.base_class import Base
from ultron8.api.db_models.sensors_trigger_types_association import (
    SENSORS_TRIGGER_TYPES_ASSOCIATION,
)
from ultron8.api.db_models.trigger import TriggerTypeDB
from ultron8.api.db_models.ultronbase import ContentPackResourceMixin, UIDFieldMixin
from ultron8.api.models.system.common import ResourceReference
from ultron8.consts import ResourceType
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

# SENSORS_TRIGGER_TYPES_ASSOCIATION = Table(
#     "sensors_trigger_types_association",
#     Base.metadata,
#     Column(
#         "sensors_packs_id", Integer(), ForeignKey("sensors.packs_id"), primary_key=True
#     ),
#     Column(
#         "trigger_types_packs_id",
#         Integer(),
#         ForeignKey("trigger_types.packs_id"),
#         primary_key=True,
#     ),
# )

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
    artifact_uri = Column("artifact_uri", String(255), nullable=True)
    poll_interval = Column("poll_interval", Integer, nullable=True)
    enabled = Column("enabled", Boolean)
    entry_point = Column("entry_point", String(255))
    description = Column("description", String(255))

    created_at = Column("created_at", String)
    updated_at = Column("updated_at", String)
    packs_id = Column("packs_id", Integer, ForeignKey("packs.id"), nullable=True)

    # trigger_types = relationship("ultron8.api.db_models.trigger.TriggerTypeDB", back_populates="sensors")

    trigger_types = relationship(
        "ultron8.api.db_models.trigger.TriggerTypeDB",
        secondary=SENSORS_TRIGGER_TYPES_ASSOCIATION,
        back_populates="sensors",
    )

    # __table_args__ = {'extend_existing': True}

    # # <><><><><><><><><><><><><><><><><><><>
    # # Sensor = LEFT side of join
    # # TriggerTypeDB = Right side of join
    # # <><><><><><><><><><><><><><><><><><><>
    # # relationship() using explicit foreign_keys, remote_side
    # # HOW TO UNDERSTAND THIS: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-viii-followers
    # trigger_types = relationship(
    #     # NOTE: is the right side entity of the relationship (the left side entity is the Sensor class).
    #     "TriggerTypeDB",
    #     # NOTE: Configures the association table that is used for this relationship, which I defined right above this class.
    #     secondary=SENSORS_TRIGGER_TYPES_ASSOCIATION,
    #     # NOTE: indicates the condition that links the left side entity (the sensor) with the association table. The join condition for the left side of the relationship is the user ID matching the sensors_packs_id field of the association table. The SENSORS_TRIGGER_TYPES_ASSOCIATION.c.sensors_packs_id expression references the sensors_packs_id column of the association table.
    #     primaryjoin=(
    #         SENSORS_TRIGGER_TYPES_ASSOCIATION.c.trigger_types_packs_id == packs_id
    #     ),
    #     # NOTE: indicates the condition that links the right side entity (the trigger_type) with the association table. This condition is similar to the one for primaryjoin, with the only difference that now I'm using sensors_packs_id, which is the other foreign key in the association table.
    #     secondaryjoin=(
    #         SENSORS_TRIGGER_TYPES_ASSOCIATION.c.sensors_packs_id == packs_id
    #     ),
    #     # NOTE: defines how this relationship will be accessed from the right side entity. From the left side, the relationship is named trigger_types, so from the right side I am going to use the name sensors to represent all the left side sensors that are linked to the trigger types in the right side. The additional lazy argument indicates the execution mode for this query. A mode of dynamic sets up the query to not run until specifically requested, which is also how I set up the posts one-to-many relationship.
    #     backref=backref("sensors", lazy="dynamic"),
    #     # backref=backref("sensors"),
    #     # foreign_keys=[packs_id],
    #     # foreign_keys=[packs_id],
    #     # foreign_keys=[SENSORS_TRIGGER_TYPES_ASSOCIATION.c.trigger_types_packs_id,
    #     # SENSORS_TRIGGER_TYPES_ASSOCIATION.c.sensors_packs_id],
    #     # NOTE: is similar to the parameter of the same name in the backref, but this one applies to the left side query instead of the right side.
    #     lazy="dynamic",
    # )

    # # SOURCE: https://stackoverflow.com/questions/28503656/attributeerror-list-object-has-no-attribute-sa-instance-state/28503775#28503775

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

    # SOURCE: https://docs.sqlalchemy.org/en/13/orm/constructors.html
    # EXAMPLE: https://github.com/haobin12358/Weidian/blob/6c1b0fd54b1ed964f4b22a356a2a66cab9d91851/WeiDian/models/model.py
    # @orm.reconstructor
    def __init__(self, *args, packs_name=None, **values):
        super(Sensors, self).__init__(*args, **values)
        self.packs_name = packs_name
        self.ref = "{}.{}".format(self.packs_name, self.class_name)
        self.uid = self.get_uid()
        self.created_at = str(datetime.datetime.utcnow())
        self.updated_at = str(datetime.datetime.utcnow())
        # self.triggers_types_packs_id = self.packs_id

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

    # # FIXME: Get this working 8/19/2019
    # def add_trigger_types(self, packs_id, data):
    #     self.trigger_types.filter_by(packs_id=packs_id).delete()
    #     tt = TriggerTypeDB(packs_name=data["name"],)

    # NOTE: source microblog
    # def add_notification(self, name, data):
    #     self.notifications.filter_by(name=name).delete()
    #     n = Notification(name=name, payload_json=json.dumps(data), user=self)
    #     db.session.add(n)
    #     return n

    # @orm.reconstructor
    # def init_on_load(self):
    #     self.packs_name = packs_name
    #     self.ref = "{}.{}".format(self.packs_name, self.class_name)
    #     self.uid = self.get_uid()
    #     self.created_at = str(datetime.datetime.utcnow())
    #     self.updated_at = str(datetime.datetime.utcnow())

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


# smoke-tests
if "__main__" == __name__:
    # from fastapi.encoders import jsonable_encoder

    # from ultron8.api import crud
    from ultron8.api.db.u_sqlite.session import db_session

    # from ultron8.api.models.sensors import SensorsBase
    # from ultron8.api.models.sensors import SensorsBaseInDB
    # from ultron8.api.models.sensors import SensorsCreate
    # from ultron8.api.models.sensors import SensorsUpdate
    # from ultron8.api.models.sensors import Sensor
    # from ultron8.api.models.sensors import SensorInDB

    # from ultron8.api.db_models.sensors import Sensors
    # from ultron8.api.db_models.sensors import SENSORS_TRIGGER_TYPES_ASSOCIATION
    # from ultron8.api.db_models.trigger import TriggerTypeDB
    # from ultron8.api.models.trigger import TriggerTypeInDBModel

    # from tests.utils.packs import create_random_packs
    # from tests.utils.trigger_instance import create_random_trigger_instance_name
    # from tests.utils.trigger_type import create_random_trigger_type
    # from tests.utils.trigger import create_random_trigger

    # from freezegun import freeze_time
    # from ultron8.debugger import debug_dump_exclude

    # from ultron8.api.models import orm_to_model

    import json

    from pydantic.json import pydantic_encoder

    #     # Initial - Setup environment vars before testing anything
    import os
    from sqlalchemy import inspect

    #     # import better_exceptions; better_exceptions.hook()

    import sys

    # from IPython.core.debugger import Tracer  # noqa
    # from IPython.core import ultratb

    # sys.excepthook = ultratb.FormattedTB(
    #     mode="Verbose", color_scheme="Linux", call_pdb=True, ostream=sys.__stdout__
    # )

    os.environ["DEBUG"] = "1"
    os.environ["TESTING"] = "1"
    os.environ["BETTER_EXCEPTIONS"] = "1"

    os.environ["DATABASE_URL"] = "sqlite:///sensors.db"
    os.environ["TEST_DATABASE_URL"] = "sqlite:///sensors.db"

    import logging

    from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

    # from ultron8.api.db.u_sqlite.session import db_session

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

    #     # Get sqlalchemy classes/objects

    from ultron8.api.db.u_sqlite.init_db import init_db
    from ultron8.api.db.u_sqlite.session import engine

    # from ultron8.api.db.u_sqlite.session import SessionLocal

    #     # make sure all SQL Alchemy models are imported before initializing DB
    #     # otherwise, SQL Alchemy might fail to initialize properly relationships
    #     # for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
    # from ultron8.api.db.u_sqlite.base import Base

    import pandas as pd

    # from ultron8.api.db_models.sensors import Sensors
    # from ultron8.api.db_models.trigger import TriggerTypeDB
    from ultron8.api.db_models.packs import Packs

    # from ultron8.api.db_models.action import Action

    print("testing")

    from faker import Faker as RealFaker
    from faker.providers import internet, file, person, lorem

    fake = RealFaker()
    fake.add_provider(internet)
    fake.add_provider(file)
    fake.add_provider(person)
    fake.add_provider(lorem)

    # import pdb

    # pdb.set_trace()
    #     # Tables should be created with Alembic migrations
    #     # But if you don't want to use migrations, create
    #     # the tables un-commenting the next line
    #     # 2 - generate database schema
    # Base.metadata.create_all(bind=engine)

    #     # 3 - create a new session
    session = db_session

    # Try initializing everything now
    # logger.info("Initializing service")
    # init()
    # logger.info("Service finished initializing")

    logger.info("Creating initial data")
    init_db(db_session)
    logger.info("Initial data created")

    import factory
    from factory import Faker

    ##########################################
    # packs
    ##########################################
    # import pdb;pdb.set_trace()

    class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            abstract = True
            sqlalchemy_session = session
            sqlalchemy_session_persistence = "commit"

    # shared_packs_name = Faker("first_name").lower()
    shared_packs_name = Faker("first_name")

    class PacksFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Packs

        # email = Faker("email")
        # hashed_password = hash_password("password123")
        # email_verified = True
        # mfa_secret = ""
        # is_active = True
        # is_superuser = False
        # id = factory.Sequence(lambda n: n)
        # name = factory.Sequence(lambda n: u'User %d' % n)
        name = Faker("first_name")
        description = Faker("sentence", nb_words=4)
        keywords = shared_packs_name
        version = "0.1.0"
        python_versions = "3"
        author = "Jarvis"
        email = Faker("email")
        contributors = "bossjones"
        files = "./tests/fixtures/simple/packs/{}".format(shared_packs_name)
        path = "./tests/fixtures/simple/packs/{}".format(shared_packs_name)
        ref = shared_packs_name

    print("try it")
    pack_random = PacksFactory()

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
