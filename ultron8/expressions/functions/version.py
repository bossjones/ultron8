# st2
import semver

__all__ = [
    "version_compare",
    "version_more_than",
    "version_less_than",
    "version_equal",
    "version_match",
    "version_bump_major",
    "version_bump_minor",
]


def version_compare(value, pattern):
    return semver.compare(value, pattern)


def version_more_than(value, pattern):
    return semver.compare(value, pattern) == 1


def version_less_than(value, pattern):
    return semver.compare(value, pattern) == -1


def version_equal(value, pattern):
    return semver.compare(value, pattern) == 0


def version_match(value, pattern):
    return semver.match(value, pattern)


def version_bump_major(value):
    return semver.bump_major(value)


def version_bump_minor(value):
    return semver.bump_minor(value)


def version_bump_patch(value):
    return semver.bump_patch(value)


def version_strip_patch(value):
    return "{major}.{minor}".format(**semver.parse(value))
