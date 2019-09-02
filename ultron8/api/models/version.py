"""
Data Models for all things having to do with Version.
"""
import logging
from datetime import datetime
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import Union

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Schema
from ultron8.api.models.base import BaseDataModel

logger = logging.getLogger(__name__)


class VersionOut(BaseDataModel):
    """
    Schema for Version.
    """

    version: str
