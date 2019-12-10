"""
Tasks init module
"""

import logging
from invoke import Collection, Context
from invoke import task
from . import core

LOGGER = logging.getLogger()

NS = Collection()
NS.add_collection(core)
