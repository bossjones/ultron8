"""
Data Models for all things having to do with Version.
"""

from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from enum import Enum
from pydantic import BaseModel, Schema, EmailStr
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class VersionOut(BaseModel):
    """
    Schema for Version.
    """

    version: str
