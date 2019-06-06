from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from ultron8.api import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
