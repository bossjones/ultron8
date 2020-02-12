"""
Data Models for all things having to do with Health.
"""
import logging

# from pydantic import BaseModel

from ultron8.api.models.base import BaseDataModel

logger = logging.getLogger(__name__)


class HealthOut(BaseDataModel):
    """
    Schema for Health.
    """

    status: str
