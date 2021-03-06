# SOURCE: https://davidemoro.blogspot.com/2014/10/sqlite-array-type-and-python-sqlalchemy.html
# I need to write up things just for remembering how I solved a particular issue if occurs in the future.
# Sqlite (with http://sqlitebrowser.org) is great for rapid prototypes development but it lacks some useful implementations provided by Postgresql (for example the sqlalchemy.dialects.postgresql.ARRAY type).
# I solved implementing a SQLAlchemy TypeDecorator with a json serialization:
# http://docs.sqlalchemy.org/en/latest/core/types.html#sqlalchemy.types.TypeDecorator
# Here it is the self-explaining code:
import datetime
from datetime import timedelta
import json
import logging
import uuid

# from sqlalchemy import String
# from sqlalchemy import DateTime
# from pyramid_sqlalchemy import BaseObject as Base
from dateutil.parser import parse as parse_date
from sqlalchemy import (
    CHAR,
    JSON,
    VARCHAR,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Sequence,
    UniqueConstraint,
    types,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql import func, operators
from sqlalchemy.types import String, TypeDecorator

from ultron8.api.db.u_sqlite.base_class import Base
from ultron8.api.db_models.ultronbase import ContentPackResourceMixin, UIDFieldMixin
from ultron8.api.models.system.common import ResourceReference
from ultron8.consts import ResourceType

LOGGER = logging.getLogger(__name__)

# NOTE: Current sqlite datatypes - https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#sqlite-data-types

# ORM Tip
# The TypeDecorator can be used to provide a consistent means of converting some type of value as it is passed into and out of the database.
# When using the ORM, a similar technique exists for converting user data from arbitrary formats which is to use the validates() decorator. This technique may be more appropriate when data coming into an ORM model needs to be normalized in some way that is specific to the business case and isn't as generic as a datatype.
# SOURCE: https://docs.sqlalchemy.org/en/13/core/custom_types.html


class ArrayType(TypeDecorator):
    """ Sqlite-like does not support arrays.
        Let's use a custom type decorator.

        See http://docs.sqlalchemy.org/en/latest/core/types.html#sqlalchemy.types.TypeDecorator
    """

    impl = String(500)

    def process_bind_param(self, value, dialect):
        """Serialize ``value`` to a JSON formatted ``str`` on the way in to DB.

        Arguments:
            value {[type]} -- [description]
            dialect {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        """Deserialize ``value`` (a ``str``, ``bytes`` or ``bytearray`` instance containing a JSON document) to a Python object on the way out of DB.

        Arguments:
            value {[type]} -- [description]
            dialect {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        return json.loads(value)

    def copy(self, **kw):
        """Produce a copy of this TypeDecorator instance.
        This is a shallow copy and is provided to fulfill part of the TypeEngine contract.
        It usually does not need to be overridden unless the user-defined TypeDecorator has local state that should be deep-copied.

        Returns:
            [type] -- [description]
        """
        return ArrayType(self.impl.length)


# NOTE: This is an example
# class Element(Base):
#     __tablename__ = 'elements'

#     id = Column(Integer(),
#                 Sequence('element_id_seq'),
#                 primary_key=True)
#     # ...
#     myarray = Column(ArrayType())


class TZDateTime(TypeDecorator):
    """Timestamps in databases should always be stored in a timezone-agnostic way. For most databases, this means ensuring a timestamp is first in the UTC timezone before it is stored, then storing it as timezone-naive (that is, without any timezone associated with it; UTC is assumed to be the "implicit" timezone). Alternatively, database-specific types like PostgreSQLs "TIMESTAMP WITH TIMEZONE" are often preferred for their richer functionality; however, storing as plain UTC will work on all databases and drivers. When a timezone-intelligent database type is not an option or is not preferred, the TypeDecorator can be used to create a datatype that convert timezone aware timestamps into timezone naive and back again. Below, Python's built-in datetime.timezone.utc timezone is used to normalize and denormalize:

    Arguments:
        TypeDecorator {[type]} -- [description]

    Raises:
        TypeError: [description]

    Returns:
        [type] -- [description]
    """

    impl = types.DateTime

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not value.tzinfo:
                raise TypeError("tzinfo is required")
            value = value.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        return value


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """

    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)


class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string.

    Usage::

        JSONEncodedDict(255)

    """

    impl = VARCHAR

    def coerce_compared_value(self, op, value):
        if op in (operators.like_op, operators.notlike_op):
            return String()
        else:
            return self

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class MyEpochType(TypeDecorator):
    impl = Integer

    epoch = datetime.date(1970, 1, 1)

    def process_bind_param(self, value, dialect):
        return (value - self.epoch).days

    def process_result_value(self, value, dialect):
        return self.epoch + timedelta(days=value)


# SOURCE: https://github.com/dodoru/pyco-sqlalchemy/blob/31b4e43fcc3b8df94c997c2ce0877ca9ce514ed9/pyco_sqlalchemy/_types.py
class DateTime(TypeDecorator):
    """
    # sample 1:
    @declared_attr
    def created_time(self):
        return db.Column(DateTime, default=datetime.utcnow)
    # sample 2:
    updated_time = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    """

    impl = types.DateTime

    def process_bind_param(self, value, dialect):
        if isinstance(value, datetime):
            return value
        elif isinstance(value, str):
            return parse_date(value)
        elif isinstance(value, (int, float)):
            return datetime.datetime.fromtimestamp(value)
        else:
            return value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        elif isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S.%f")


# ##################################################################################################
# # SOURCE: https://github.com/valleygtc/meme-manager/blob/master/src/meme_manager/models.py
# # NOTE: I think this works but I haven't tried it yet
# ##################################################################################################
# class Array(types.TypeDecorator):
#     """Store as TEXT, seperated by comma.
#     """

#     impl = types.Text

#     def coerce_compared_value(self, op, value):
#         # support <column>.contains(<str>)
#         if op in (operators.contains_op, operators.like_op, operators.notlike_op):
#             return String()
#         else:
#             return self

#     def process_bind_param(self, value, dialect):
#         """
#         value [list]
#         return text [str]
#         """
#         return ','.join(value)

#     def process_result_value(self, value, dialect):
#         """
#         value [str]
#         return array [list]
#         """
#         rv = value.split(',') if value else []
#         return rv

#     def copy(self, **kw):
#         return Array(self.impl.length)


# class Image(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.LargeBinary(length=2**24-1), nullable=False) # max size: 16MB
#     img_type = db.Column(db.String(64), nullable=False)
#     tags = db.Column(Array(), nullable=False)
#     group_id = db.Column(db.Integer, db.ForeignKey(Group.id))
#     group = db.relationship(Group, backref=db.backref('images', lazy=True, cascade="all,delete"))
#     create_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())

#     def readyToJSON(self, keys, datetime_format):
#         """
#         Params:
#             keys [Iterable[str]]
#             datetime_format [str]: 同datetime.strptime()的格式声明
#         """
#         d = {}
#         for k in keys:
#             if k == 'create_at':
#                 v = getattr(self, k).strftime(datetime_format)
#             elif k == 'group':
#                 v = self.group.name if self.group else None
#             else:
#                 v = getattr(self, k)
#             d[k] = v
#         return d

#     def __repr__(self):
#         return '<Image %r>' % self.id
# ##################################################################################################
# # SOURCE: https://github.com/valleygtc/meme-manager/blob/master/src/meme_manager/models.py
# # NOTE: I think this works but I haven't tried it yet
# ##################################################################################################
