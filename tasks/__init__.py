# pylint: disable=wrong-import-position, wrong-import-order, invalid-name
"""
Invoke build script.
Show all tasks with::
    invoke -l
.. seealso::
    * http://pyinvoke.org
    * https://github.com/pyinvoke/invoke
"""

import logging
from invoke import Collection, Context
from invoke import task
from . import core
from . import local

LOGGER = logging.getLogger()

ns = Collection()
ns.add_collection(core)
ns.add_collection(local)

# https://github.com/imbrra/logowanie/blob/38a1a38ea9f5b2494e5bc986df651ff9d713fda5/tasks/__init__.py
