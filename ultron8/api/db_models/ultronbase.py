from __future__ import absolute_import

import abc
import datetime

import six
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from ultron8.api import settings
from ultron8.api.db.u_sqlite.base_class import Base
from ultron8.api.db_models.utils import key_not_string
from ultron8.api.db_models.utils import ProxiedDictMixin
from ultron8.api.models.system.common import ResourceReference
from ultron8.consts import ResourceType
from sqlalchemy import orm

# from ultron8.api.models.system.base import DictSerializableClassMixin
# from sqlalchemy.orm import relationship
# from ultron8.api.db.u_sqlite.session import db_session

JSON_UNFRIENDLY_TYPES = datetime.datetime

# SOURCE: https://github.com/cburmeister/flask-bones/blob/master/app/database.py
# class CRUDMixin(object):
#     __table_args__ = {'extend_existing': True}

#     id = db.Column(db.Integer, primary_key=True)

#     @classmethod
#     def get_by_id(cls, id):
#         if any((isinstance(id, str) and id.isdigit(),
#                 isinstance(id, (int, float))),):
#             return cls.query.get(int(id))
#         return None

#     @classmethod
#     def create(cls, **kwargs):
#         instance = cls(**kwargs)
#         return instance.save()

#     def update(self, commit=True, **kwargs):
#         for attr, value in kwargs.items():
#             setattr(self, attr, value)
#         return commit and self.save() or self

#     def save(self, commit=True):
#         db.session.add(self)
#         if commit:
#             db.session.commit()
#         return self

#     def delete(self, commit=True):
#         db.session.delete(self)
#         return commit and db.session.commit()


class UltronFoundationDB(ProxiedDictMixin):
    """
    Base abstraction for a model entity. This foundation class should only be directly
    inherited from the application domain models.
    """

    # Variable representing a type of this resource
    RESOURCE_TYPE = ResourceType.UNKNOWN

    # def __init__(self, name):
    #     self.name = name

    # def __repr__(self):
    #     return "RuleType(%r)" % self.name

    def mask_secrets(self, value):
        """
        Process the object and mask secret values.

        :type value: ``dict``
        :param value: Document dictionary.

        :rtype: ``dict``
        """
        return value

    def to_serializable_dict(self, mask_secrets=False):
        """
        Serialize object to a dictionary which can be serialized as JSON.

        :param mask_secrets: True to mask secrets in the resulting dict.
        :type mask_secrets: ``boolean``

        :rtype: ``dict``
        """
        raise NotImplementedError()

    # def __str__(self):
    #     attrs = list()
    #     for k in sorted(self._proxied.keys()):
    #         v = getattr(self, k)
    #         v = '"%s"' % str(v) if type(v) in [str, six.text_type, datetime.datetime] else str(v)
    #         attrs.append('%s=%s' % (k, v))
    #     return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def get_resource_type(self):
        return self.RESOURCE_TYPE


# class UltronBaseDB(UltronFoundationDB):
#     """Abstraction for a user content model."""

#     name = Column(String, unique=True, required=True)
#     description = Column(String)

# class EscapedDictField(me.DictField):

#     def to_python(self, value):
#         value = super(EscapedDictField, self).to_python(value)
#         return value

#     def validate(self, value):
#         if not isinstance(value, dict):
#             self.error('Only dictionaries may be used in a DictField')
#         if key_not_string(value):
#             self.error("Invalid dictionary key - documents must have only string keys")
#         me.base.ComplexBaseField.validate(self, value)


# class EscapedDynamicField(me.DynamicField):

#     def to_mongo(self, value, use_db_field=True, fields=None):
#         value = mongoescape.escape_chars(value)
#         return super(EscapedDynamicField, self).to_mongo(value=value, use_db_field=use_db_field,
#                                                          fields=fields)

#     def to_python(self, value):
#         value = super(EscapedDynamicField, self).to_python(value)
#         return mongoescape.unescape_chars(value)


# class TagField(me.EmbeddedDocument):
#     """
#     To be attached to a db model object for the purpose of providing supplemental
#     information.
#     """
#     name = me.StringField(max_length=1024)
#     value = me.StringField(max_length=1024)


# class TagsMixin(object):
#     """
#     Mixin to include tags on an object.
#     """
#     tags = me.ListField(field=me.EmbeddedDocumentField(TagField))

#     @classmethod
#     def get_indexes(cls):
#         return ['tags.name', 'tags.value']


# class RefFieldMixin(object):
#     """
#     Mixin class which adds "ref" field to the class inheriting from it.
#     """

#     ref = me.StringField(required=True, unique=True)

# SOURCE: https://docs.sqlalchemy.org/en/13/orm/inheritance.html ?
class UIDFieldMixin(object):
    """
    Mixin class which adds "uid" field to the class inheriting from it.

    UID field is a unique identifier which we can be used to unambiguously reference a resource in
    the system.
    """

    UID_SEPARATOR = ":"

    RESOURCE_TYPE = abc.abstractproperty
    UID_FIELDS = abc.abstractproperty

    # uid = me.StringField(required=True)

    # @classmethod
    # def get_indexes(cls):
    #     # Note: We use a special sparse index so we don't need to pre-populate "uid" for existing
    #     # models in the database before ensure_indexes() is called.
    #     # This field gets populated in the constructor which means it will be lazily assigned next
    #     # time the model is saved (e.g. once register-content is ran).
    #     indexes = [
    #         {
    #             'fields': ['uid'],
    #             'unique': True,
    #             'sparse': True
    #         }
    #     ]
    #     return indexes

    # SOURCE: https://docs.sqlalchemy.org/en/13/orm/constructors.html
    # EXAMPLE: https://github.com/haobin12358/Weidian/blob/6c1b0fd54b1ed964f4b22a356a2a66cab9d91851/WeiDian/models/model.py
    # @orm.reconstructor
    def get_uid(self):
        """
        Return an object UID constructed from the object properties / fields.

        :rtype: ``str``
        """
        parts = []
        parts.append(self.RESOURCE_TYPE)

        for field in self.UID_FIELDS:
            value = getattr(self, field, None) or ""
            parts.append(value)

        uid = self.UID_SEPARATOR.join(parts)
        return uid

    # SOURCE: https://docs.sqlalchemy.org/en/13/orm/constructors.html
    # EXAMPLE: https://github.com/haobin12358/Weidian/blob/6c1b0fd54b1ed964f4b22a356a2a66cab9d91851/WeiDian/models/model.py
    # @orm.reconstructor
    def get_uid_parts(self):
        """
        Return values for fields which make up the UID.

        :rtype: ``list``
        """
        parts = self.uid.split(self.UID_SEPARATOR)  # pylint: disable=no-member
        parts = [part for part in parts if part.strip()]
        return parts

    # SOURCE: https://docs.sqlalchemy.org/en/13/orm/constructors.html
    # EXAMPLE: https://github.com/haobin12358/Weidian/blob/6c1b0fd54b1ed964f4b22a356a2a66cab9d91851/WeiDian/models/model.py
    # @orm.reconstructor
    def has_valid_uid(self):
        """
        Return True if object contains a valid id (aka all parts contain a valid value).

        :rtype: ``bool``
        """
        parts = self.get_uid_parts()
        return len(parts) == len(self.UID_FIELDS) + 1


class ContentPackResourceMixin(object):
    """
    Mixin class provides utility methods for models which belong to a pack.
    """

    # metadata_file = me.StringField(
    #     required=False,
    #     help_text=('Path to the metadata file (file on disk which contains resource definition) '
    #                'relative to the pack directory.'))

    def get_pack_uid(self):
        """
        Return an UID of a pack this resource belongs to.

        :rtype ``str``
        """
        parts = [ResourceType.PACK, self.pack]
        uid = UIDFieldMixin.UID_SEPARATOR.join(parts)
        return uid

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

    # @classmethod
    # def get_indexes(cls):
    #     return [
    #         {
    #             'fields': ['metadata_file'],
    #         }
    #     ]


# class ChangeRevisionFieldMixin(object):

#     rev = me.IntField(required=True, default=1)

#     @classmethod
#     def get_indexes(cls):
#         return [
#             {
#                 'fields': ['id', 'rev'],
#                 'unique': True
#             }
#         ]
