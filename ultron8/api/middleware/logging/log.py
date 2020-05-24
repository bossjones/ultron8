from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import codecs
import json
import logging
import logging.config

from ultron8.api import settings
from ultron8.yaml import yaml
from ultron8.yaml import yaml_load
from collections import OrderedDict

# import daiquiri
# import daiquiri.formatter


LOGSEVERITY = {
    "CRITICAL": 50,
    "FATAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "WARN": 30,
    "INFO": 20,
    "DEBUG": 10,
    "NOTSET": 0,
}

# FMT_DEFAULT = "%(asctime)s [PID=%(process)d] [LEVEL=%(levelname)s] [NAME=%(name)s] - [THREAD=%(threadName)s] "
# " [ProcessName=%(processName)s] "
# "- [%(filename)s:%(lineno)s -  %(funcName)20s() ] -> [MSG=%(message)s]"

# # SOURCE: https://docs.python.org/2/library/stdtypes.html#string-formatting
# # SOURCE: https://docs.python.org/3/library/logging.html?highlight=funcname
# # SOURCE: https://stackoverflow.com/questions/251464/how-to-get-a-function-name-as-a-string-in-python
# # EXAMPLE: 2019-07-24 19:34:01,459 __main__ INFO     PID: 32808 THREAD: MainThread ProcessName: MainProcess FILE: dev_serve.py:55 FUNCTION: <module>  [DEBUG] True
# FMT_SIMPLE = "%(asctime)-15s %(name)-5s %(levelname)-8s "
# "PID: %(process)d THREAD: %(threadName)s ProcessName: %(processName)s "
# "FILE: %(filename)s:%(lineno)s FUNCTION: %(funcName)s %(message)s"


# def setup_logging(level=None, outputs=None, fmt=FMT_SIMPLE):
#     """Configure logging."""
#     if not level:
#         level = settings.LOG_LEVEL
#     if not outputs:
#         # outputs = (daiquiri.output.STDOUT,)
#         outputs = (
#             daiquiri.output.Stream(
#                 formatter=daiquiri.formatter.ColorFormatter(fmt=fmt)
#             ),
#         )
#     daiquiri.setup(level=level, outputs=outputs)


# def get_logger_modules():
#     import logging

#     for key in logging.Logger.manager.loggerDict:
#         print(key)


# # datefmt='%Y-%m-%d %H:%M:%S'

# logger = daiquiri.getLogger(__name__)
# logger.info("It works with a custom format!")


def get_yaml_config() -> OrderedDict:
    HERE = os.path.abspath(os.path.dirname(__file__))
    config_file = "log_config.yml"
    config_path = os.path.join(HERE, config_file)
    config = yaml_load(config_path, ordered=True)
    return config


def setup_logging() -> None:
    """Configure logging."""
    log_config = get_yaml_config()

    # set up proper logging. This one disables the previously configured loggers.
    logging.config.dictConfig(log_config)


# create the logger object
logger = logging.getLogger(__name__)
# https://stackoverflow.com/questions/1987468/determining-if-root-logger-is-set-to-debug-level-in-python
root_logger = logging.getLogger().isEnabledFor(settings.LOG_LEVEL)
logger.info("It works with a custom format!")

# SMOKE-TESTS
if __name__ == "__main__":
    setup_logging()
    from logging_tree import printout

    logger.info("TESTING TESTING 1-2-3")
    printout()
