import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from tests.api.api_v1.test_login import test_get_access_token
from ultron8.api.db.u_sqlite.session import SessionLocal

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.DEBUG),
    after=after_log(logger, logging.WARN),
)
def init():
    try:
        # Try to create session to check if DB is awake
        db = SessionLocal()
        db.execute("SELECT 1")
        # Wait for API to be awake, run one simple tests to authenticate
        test_get_access_token()
    except Exception as e:
        logger.error(e)
        raise e


def main():
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
