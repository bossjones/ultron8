import logging

from ultron8.api.db.u_sqlite.init_db import init_db
from ultron8.api.db.u_sqlite.session import db_session

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init():
    init_db(db_session)


def main():
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
