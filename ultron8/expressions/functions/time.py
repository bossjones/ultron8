# st2common

import six

import datetime

__all__ = ["to_human_time_from_seconds"]

long_int = int


def to_human_time_from_seconds(seconds):
    """
    Given a time value in seconds, this function returns
    a fuzzy version like 3m5s.

    :param time_seconds: Time specified in seconds.
    :type time_seconds: ``int`` or ``long`` or ``float``

    :rtype: ``str``
    """
    assert (
        isinstance(seconds, int)
        or isinstance(seconds, int)
        or isinstance(seconds, float)
    )

    return _get_human_time(seconds)


def _get_human_time(seconds):
    """
    Takes number of seconds as input and returns a string of form '1h3m5s'.

    :param seconds: Number of seconds.
    :type seconds: ``int`` or ``long`` or ``float``

    :rtype: ``str``
    """

    if seconds is None:
        return None

    if seconds == 0:
        return "0s"

    if seconds < 1:
        return "%s\u03BCs" % seconds  # Microseconds

    if isinstance(seconds, float):
        seconds = long_int(round(seconds))  # Let's lose microseconds.

    timedelta = datetime.timedelta(seconds=seconds)
    offset_date = datetime.datetime(1, 1, 1) + timedelta

    years = offset_date.year - 1
    days = offset_date.day - 1
    hours = offset_date.hour
    mins = offset_date.minute
    secs = offset_date.second

    time_parts = [years, days, hours, mins, secs]

    first_non_zero_pos = next((i for i, x in enumerate(time_parts) if x), None)

    if first_non_zero_pos is None:
        return "0s"
    else:
        time_parts = time_parts[first_non_zero_pos:]

    if len(time_parts) == 1:
        return "%ss" % tuple(time_parts)
    elif len(time_parts) == 2:
        return "%sm%ss" % tuple(time_parts)
    elif len(time_parts) == 3:
        return "%sh%sm%ss" % tuple(time_parts)
    elif len(time_parts) == 4:
        return "%sd%sh%sm%ss" % tuple(time_parts)
    elif len(time_parts) == 5:
        return "%sy%sd%sh%sm%ss" % tuple(time_parts)
