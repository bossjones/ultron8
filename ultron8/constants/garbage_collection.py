# st2common

__all__ = [
    "DEFAULT_COLLECTION_INTERVAL",
    "DEFAULT_SLEEP_DELAY",
    "MINIMUM_TTL_DAYS",
    "MINIMUM_TTL_DAYS_EXECUTION_OUTPUT",
]


# Default garbage collection interval (in seconds)
DEFAULT_COLLECTION_INTERVAL = 600

# How to long to wait / sleep between collection of different object types (in seconds)
DEFAULT_SLEEP_DELAY = 2

# Minimum value for the TTL. If user supplies value lower than this, we will throw.
MINIMUM_TTL_DAYS = 7

# Minimum TTL in days for action execution output objects.
MINIMUM_TTL_DAYS_EXECUTION_OUTPUT = 1
