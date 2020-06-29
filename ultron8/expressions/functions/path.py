# st2
import os

__all__ = ["basename", "dirname"]


def basename(path):
    return os.path.basename(path)


def dirname(path):
    return os.path.dirname(path)
