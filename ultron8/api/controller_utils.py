"""Basic utility module for Api service."""
import logging
from datetime import datetime
from datetime import timedelta

from starlette.exceptions import HTTPException

log = logging.getLogger(__name__)


def validate_guid(guid: str) -> bool:
    """Validates that a guid is formatted properly"""
    valid_chars = set("0123456789abcdef")
    count = 0
    for char in guid:
        count += 1
        if char not in valid_chars or count > 32:
            raise ValueError("Invalid GUID format.")
    if count != 32:
        raise ValueError("Invalid GUID format.")
    return guid


def transform_to_bool(value):
    """
    Transforms a certain set of values to True or False.
    True can be represented by '1', 'True' and 'true.'
    False can be represented by '1', 'False' and 'false.'

    Any other representation will be rejected.
    """
    if value in ["1", "true", "True", True]:
        return True
    elif value in ["0", "false", "False", False]:
        return False
    raise ValueError('Invalid bool representation "%s" provided.' % value)
