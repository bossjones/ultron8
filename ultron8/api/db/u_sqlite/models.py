"""Define sqlite tables."""
import logging
from datetime import datetime, timedelta
import sqlalchemy

log = logging.getLogger(__name__)

# Database table definitions.
# metadata = sqlalchemy.MetaData()

# guid_tracker = sqlalchemy.Table(
#     "guid_tracker",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
#     sqlalchemy.Column("name", sqlalchemy.String),
#     sqlalchemy.Column("expire", sqlalchemy.DateTime),
# )
