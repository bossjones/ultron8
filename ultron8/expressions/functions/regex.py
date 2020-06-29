# st2common
import re
import six

__all__ = ["regex_match", "regex_replace", "regex_search", "regex_substring"]


def _get_regex_flags(ignorecase=False):
    return re.I if ignorecase else 0


def regex_match(value, pattern, ignorecase=False):
    if not isinstance(value, six.string_types):
        value = str(value)
    flags = _get_regex_flags(ignorecase)
    return bool(re.match(pattern, value, flags))


def regex_replace(value, pattern, replacement, ignorecase=False):
    if not isinstance(value, six.string_types):
        value = str(value)
    flags = _get_regex_flags(ignorecase)
    regex = re.compile(pattern, flags)
    return regex.sub(replacement, value)


def regex_search(value, pattern, ignorecase=False):
    if not isinstance(value, six.string_types):
        value = str(value)
    flags = _get_regex_flags(ignorecase)
    return bool(re.search(pattern, value, flags))


def regex_substring(value, pattern, result_index=0, ignorecase=False):
    if not isinstance(value, six.string_types):
        value = str(value)
    flags = _get_regex_flags(ignorecase)
    return re.findall(pattern, value, flags)[result_index]
