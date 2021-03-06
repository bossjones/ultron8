from __future__ import unicode_literals

import six

# SOURCE: https://docs.sqlalchemy.org/en/13/_modules/examples/vertical/dictlike.html


class ProxiedDictMixin(object):
    """Adds obj[key] access to a mapped class.

    This class basically proxies dictionary access to an attribute
    called ``_proxied``.  The class which inherits this class
    should have an attribute called ``_proxied`` which points to a dictionary.

    """

    def __len__(self):
        return len(self._proxied)

    def __iter__(self):
        return iter(self._proxied)

    def __getitem__(self, key):
        return self._proxied[key]

    def __contains__(self, key):
        return key in self._proxied

    def __setitem__(self, key, value):
        self._proxied[key] = value

    def __delitem__(self, key):
        del self._proxied[key]


# SOURCE: https://github.com/MongoEngine/mongoengine/blob/82f0eb1cbc7b068b643df690680cd1dd5424f529/mongoengine/fields.py
def key_not_string(d):
    """Helper function to recursively determine if any key in a
    dictionary is not a string.
    """
    for k, v in d.items():
        if not isinstance(k, six.string_types) or (
            isinstance(v, dict) and key_not_string(v)
        ):
            return True


# class AlchemyJsonEncoder(json.JSONEncoder):
#     """
#     Class for serializing SQLAlchemy class. It will serialize SQLAlchemy object to a json object.
#     """
#     def default(self, obj):
#         if isinstance(obj.__class__, DeclarativeMeta):
#             # an SQLAlchemy class
#             fields = {}
#             for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
#                 data = obj.__getattribute__(field)
#                 try:
#                     # convert timestamp to unix timestamp to avoid type error Exception
#                     if isinstance(data, datetime):
#                         data = time.mktime(data.timetuple())
#                     # this will fail on non-encodable values, like other classes
#                     json.dumps(data)
#                     fields[field] = data
#                 except TypeError:
#                     logger.info("Unsupported data type when dumping to json!")
#                     fields[field] = None

#             return fields

#         return json.JSONEncoder.default(self, obj)
