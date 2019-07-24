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


def setup_logging(level=None, outputs=None):
    """Configure logging."""
    if not level:
        level = settings.LOG_LEVEL
    if not outputs:
        # outputs = (daiquiri.output.STDOUT,)
        outputs = (
            daiquiri.output.Stream(
                formatter=daiquiri.formatter.ColorFormatter(
                    fmt="%(asctime)s [PID=%(process)d] [LEVEL=%(levelname)s] [NAME=%(name)s] - [THREAD=%(threadName)s] "
                    " [ProcessName=%(processName)s] "
                    "- [%(filename)s:%(lineno)s -  %(funcName)20s() ] -> [MSG=%(message)s]"
                )
            ),
        )
        # FIXME: TRY THIS LOGGING FORMAT # [%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s

        # outputs = (
        #     daiquiri.output.Stream(formatter=daiquiri.formatter.ColorFormatter(
        #         fmt="%(asctime)s [PID=%(process)d] [LEVEL=%(levelname)s] [NAME=%(name)s] - [THREAD=%(threadName)s] "
        #         " [PATH=%(pathname)s] [ProcessName=%(processName)s] "
        #         "- [%(filename)s:%(lineno)s -  %(funcName)20s() ] -> [MSG=%(message)s]")),
        # )
    daiquiri.setup(level=level, outputs=outputs)


# datefmt='%Y-%m-%d %H:%M:%S'

logger = daiquiri.getLogger(__name__)
logger.info("It works with a custom format!")
