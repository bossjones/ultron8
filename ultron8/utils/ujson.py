# st2common

import copy

import ujson

__all__ = ["fast_deepcopy"]


def fast_deepcopy(value, fall_back_to_deepcopy=True):
    """
    Perform a fast deepcopy of the provided value.

    :param fall_back_to_deepcopy: True to fall back to copy.deepcopy() in case ujson throws an
                                  exception.
    :type fall_back_to_deepcopy: ``bool``
    """
    # NOTE: ujson round-trip is up to 10 times faster on smaller and larger dicts compared
    # to copy.deepcopy(), but it has some edge cases with non-simple types such as datetimes -
    try:
        value = ujson.loads(ujson.dumps(value))
    except (OverflowError, ValueError) as e:
        # NOTE: ujson doesn't support 5 or 6 bytes utf-8 sequences which we use
        # in our tests so we fall back to deep copy
        if not fall_back_to_deepcopy:
            raise e

        value = copy.deepcopy(value)

    return value
