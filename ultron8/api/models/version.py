"""
Data Models for all things having to do with Version.
"""
import logging


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
