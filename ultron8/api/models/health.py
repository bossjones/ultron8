"""
Data Models for all things having to do with Health.
"""
import logging

from ultron8.api.models.base import BaseDataModel

# from pydantic import BaseModel


logger = logging.getLogger(__name__)


class HealthOut(BaseDataModel):
    """
    Schema for Health.
    """

    status: str
