# st2
import ast
import json

import six

from ultron8.expressions.functions import data

# from ultron8.utils.compat import to_unicode


def _cast_object(x):
    """
    Method for casting string to an object (dict) or array.

    Note: String can be either serialized as JSON or a raw Python output.
    """
    x = _cast_none(x)

    if isinstance(x, six.string_types):
        try:
            return json.loads(x)
        except:
            return ast.literal_eval(x)
    else:
        return x


def _cast_boolean(x):
    x = _cast_none(x)

    if isinstance(x, six.string_types):
        return ast.literal_eval(x.capitalize())

    return x


def _cast_integer(x):
    x = _cast_none(x)
    x = int(x)
    return x


def _cast_number(x):
    x = _cast_none(x)
    x = float(x)
    return x


def _cast_string(x):
    if x is None:
        # Preserve None as-is
        return x

    if not isinstance(x, six.string_types):
        value_type = type(x).__name__
        msg = 'Value "%s" must either be a string or None. Got "%s".' % (x, value_type)
        raise ValueError(msg)

    # x = to_unicode(x)
    x = _cast_none(x)
    return x


def _cast_none(x):
    """
    Cast function which serializes special magic string value which indicate "None" to None type.
    """
    if isinstance(x, six.string_types) and x == data.NONE_MAGIC_VALUE:
        return None

    return x


# These types as they appear in json schema.
CASTS = {
    "array": _cast_object,
    "boolean": _cast_boolean,
    "integer": _cast_integer,
    "number": _cast_number,
    "object": _cast_object,
    "string": _cast_string,
}


def get_cast(cast_type):
    """
    Determines the callable which will perform the cast given a string representation
    of the type.

    :param cast_type: Type of the cast to perform.
    :type cast_type: ``str``

    :rtype: ``callable``
    """
    return CASTS.get(cast_type, None)
