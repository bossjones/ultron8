# st2common

__all__ = [
    "ALLOWED_SCOPES",
    "SYSTEM_SCOPE",
    "FULL_SYSTEM_SCOPE",
    "SYSTEM_SCOPES",
    "USER_SCOPE",
    "FULL_USER_SCOPE",
    "USER_SCOPES",
    "USER_SEPARATOR",
    "DATASTORE_SCOPE_SEPARATOR",
    "DATASTORE_KEY_SEPARATOR",
]

ALL_SCOPE = "all"

# Parent namespace for all items in key-value store
DATASTORE_PARENT_SCOPE = "u8kv"
DATASTORE_SCOPE_SEPARATOR = (
    "."  # To separate scope from datastore namespace. E.g. u8kv.system
)

# Namespace to contain all system/global scoped variables in key-value store.
SYSTEM_SCOPE = "system"
FULL_SYSTEM_SCOPE = "%s%s%s" % (
    DATASTORE_PARENT_SCOPE,
    DATASTORE_SCOPE_SEPARATOR,
    SYSTEM_SCOPE,
)

SYSTEM_SCOPES = [SYSTEM_SCOPE]

# Namespace to contain all user scoped variables in key-value store.
USER_SCOPE = "user"
FULL_USER_SCOPE = "%s%s%s" % (
    DATASTORE_PARENT_SCOPE,
    DATASTORE_SCOPE_SEPARATOR,
    USER_SCOPE,
)

USER_SCOPES = [USER_SCOPE]

USER_SEPARATOR = ":"

# Separator for keys in the datastore
DATASTORE_KEY_SEPARATOR = ":"

ALLOWED_SCOPES = [SYSTEM_SCOPE, USER_SCOPE, FULL_SYSTEM_SCOPE, FULL_USER_SCOPE]
