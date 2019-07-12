import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from ultron8.api import settings

logger = logging.getLogger(__name__)


def configure_engine(*args, **kwargs):
    args_with_defaults = [f"{settings.DATABASE_URL}?check_same_thread=False"].extend(
        args
    )
    kwargs_with_defaults = dict({"pool_pre_ping": True}, **kwargs)
    return create_engine(*args_with_defaults, **kwargs_with_defaults)


# By default, check_same_thread is True and only the creating thread may use the connection. If set False, the returned connection may be shared across multiple threads. When using multiple threads with the same connection writing operations should be serialized by the user to avoid data corruption.
engine = create_engine(
    f"{settings.DATABASE_URL}?check_same_thread=False", pool_pre_ping=True, echo=True
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
