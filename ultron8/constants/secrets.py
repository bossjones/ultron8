# st2common

__all__ = ["MASKED_ATTRIBUTES_BLACKLIST", "MASKED_ATTRIBUTE_VALUE"]

# A blacklist of attributes which should be masked in the log messages by default.
# Note: If an attribute is an object or a dict, we try to recursively process it and mask the
# values.
MASKED_ATTRIBUTES_BLACKLIST = [
    "password",
    "auth_token",
    "token",
    "secret",
    "credentials",
    "st2_auth_token",
]

# Value with which the masked attribute values are replaced
MASKED_ATTRIBUTE_VALUE = "********"
