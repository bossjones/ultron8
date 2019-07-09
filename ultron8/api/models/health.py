"""
Data Models for all things having to do with Health.
"""
import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class HealthOut(BaseModel):
    """
    Schema for Health.
    """

    status: str
