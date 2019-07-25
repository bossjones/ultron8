import daiquiri
import daiquiri.formatter

from ultron8.api import settings

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

FMT_DEFAULT = "%(asctime)s [PID=%(process)d] [LEVEL=%(levelname)s] [NAME=%(name)s] - [THREAD=%(threadName)s] "
" [ProcessName=%(processName)s] "
"- [%(filename)s:%(lineno)s -  %(funcName)20s() ] -> [MSG=%(message)s]"

# SOURCE: https://docs.python.org/2/library/stdtypes.html#string-formatting
# SOURCE: https://docs.python.org/3/library/logging.html?highlight=funcname
# SOURCE: https://stackoverflow.com/questions/251464/how-to-get-a-function-name-as-a-string-in-python
# EXAMPLE: 2019-07-24 19:34:01,459 __main__ INFO     PID: 32808 THREAD: MainThread ProcessName: MainProcess FILE: dev_serve.py:55 FUNCTION: <module>  [DEBUG] True
FMT_SIMPLE = "%(asctime)-15s %(name)-5s %(levelname)-8s "
"PID: %(process)d THREAD: %(threadName)s ProcessName: %(processName)s "
"FILE: %(filename)s:%(lineno)s FUNCTION: %(funcName)s %(message)s"


def setup_logging(level=None, outputs=None, fmt=FMT_SIMPLE):
    """Configure logging."""
    if not level:
        level = settings.LOG_LEVEL
    if not outputs:
        # outputs = (daiquiri.output.STDOUT,)
        outputs = (
            daiquiri.output.Stream(
                formatter=daiquiri.formatter.ColorFormatter(fmt=fmt)
            ),
        )
    daiquiri.setup(level=level, outputs=outputs)


# datefmt='%Y-%m-%d %H:%M:%S'

logger = daiquiri.getLogger(__name__)
logger.info("It works with a custom format!")
