"""
Data Models for all things having to do with Health.
"""
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


class HealthOut(BaseModel):
    """
    Schema for Health.
    """

    status: str
