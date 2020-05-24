"""
Data Models for all things having to do with Version.
"""
from datetime import datetime
from enum import Enum
import logging

from typing import Dict, List, Optional, Sequence, Set, Tuple, Union

from pydantic import BaseModel, Schema

from ultron8.api.models.base import BaseDataModel

# SOURCE: https://github.com/tiangolo/fastapi/issues/634
try:
    from pydantic import EmailStr
except ImportError:
    from pydantic.networks import EmailStr


logger = logging.getLogger(__name__)


class VersionOut(BaseDataModel):
    """
    Schema for Version.
    """

    version: str
