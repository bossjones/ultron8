# SOURCE: https://github.com/bergran/fast-api-project-template/blob/master/README.md

"""New and improved access token data object, used with jwt to accurately record scopes and expirations in the database"""

import logging
import datetime
from uuid import uuid4

# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import Column, Integer, String, ForeignKey

# from sqlalchemy.dialects.postgresql import ARRAY

from ultron8.api.db_models.types import ArrayType, DateTime

# from enum import Enum
# from enum import IntEnum
# from typing import Dict
# from typing import List
# from typing import Optional
# from typing import Sequence
# from typing import Set
# from typing import Tuple
# from typing import Union

# from pydantic import BaseModel

# # SOURCE: https://github.com/tiangolo/fastapi/issues/634
# try:
#     from pydantic import EmailStr
# except ImportError:
#     from pydantic.networks import EmailStr

# from pydantic import Schema

from ultron8.api.models.base import BaseDataModel

# from ultron8.api.models.packs import

log = logging.getLogger(__name__)


class AccessToken(BaseDataModel):
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    modified = Column(DateTime, default=datetime.datetime.utcnow)
    app = Column(Integer, ForeignKey("app.id"))
    scopes = Column(ArrayType(String), default=[])
    access_token = Column(String(36), default=uuid4)
