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

# NOTE: https://docs.sqlalchemy.org/en/13/orm/contextual.html
# A scoped_session is constructed by calling it, passing it a factory which can create new Session objects. A factory is just something that produces a new object when called, and in the case of Session, the most common factory is the sessionmaker
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
