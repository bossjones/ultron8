import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from ultron8.api import settings

logger = logging.getLogger(__name__)

###############################################################
# NOTE: Regarding "check_same_thread=False"
###############################################################
# According to sqlite3.connect:
# By default, check_same_thread is True and only the creating thread may use the connection. If set False, the returned connection may be shared across multiple threads. When using multiple threads with the same connection writing operations should be serialized by the user to avoid data corruption.
###############################################################


def configure_engine(*args, **kwargs):
    args_with_defaults = [f"{settings.DATABASE_URL}?check_same_thread=False"].extend(
        args
    )
    kwargs_with_defaults = dict({"pool_pre_ping": True}, **kwargs)
    return create_engine(*args_with_defaults, **kwargs_with_defaults)


###############################################################
# Technical details
# SOURCE: https://fastapi.tiangolo.com/tutorial/sql-databases/
###############################################################
# By default SQLite will only allow one thread to communicate with it, assuming that each thread would handle an independent request.

# This is to prevent accidentally sharing the same connection for different things (for different requests).

# But in FastAPI, using normal functions (def) more than one thread could interact with the database for the same request, so we need to make SQLite know that it should allow that with connect_args={"check_same_thread": False}.

# Also, we will make sure each request gets its own database connection session in a dependency, so there's no need for that default mechanism.


# By default, check_same_thread is True and only the creating thread may use the connection. If set False, the returned connection may be shared across multiple threads. When using multiple threads with the same connection writing operations should be serialized by the user to avoid data corruption.
engine = create_engine(
    f"{settings.DATABASE_URL}?check_same_thread=False", pool_pre_ping=True, echo=True
)

# NOTE: https://docs.sqlalchemy.org/en/13/orm/contextual.html
# A scoped_session is constructed by calling it, passing it a factory which can create new Session objects. A factory is just something that produces a new object when called, and in the case of Session, the most common factory is the sessionmaker
# NOTE: SQLAlchemy (and in this case SQLite also) doesn't work if you share a session across threads. You may not be using threads explicitly, but mod_wsgi is, and you've defined a global session object. Either use scoped_session to handle creating a unique session for each thread. (https://stackoverflow.com/questions/34009296/using-sqlalchemy-session-from-flask-raises-sqlite-objects-created-in-a-thread-c)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# FIXME: We name it SessionLocal to distinguish it from the Session we are importing from SQLAlchemy.
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
