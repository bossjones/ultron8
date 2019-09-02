"""Pydantic serializers for managing (de)serializationand doc generation."""
import logging
from datetime import datetime
from datetime import time
from datetime import timedelta
from datetime import timezone
from typing import Optional
from typing import Type
from typing import Union

from pydantic import BaseModel
from pydantic import validator
from ultron8.api.models.base import BaseDataModel

log = logging.getLogger(__name__)


# Properties to receive on item creation
class GuidCreate(BaseDataModel):
    name: str


class GuidIn(BaseDataModel):
    """
    Serializer for creating a record.

    Formats data, so that it'll play nicely  w/ the DB.

    Also, sets defaults for `expire`.
    """

    expire: datetime = None
    name: str

    @validator("expire", pre=True, always=True)
    def set_expire(cls, v):
        """Set expire time as 30 days from now, if not specified."""
        if v is None:
            return datetime.now(timezone.utc) + timedelta(days=30)
        return v

    @validator("expire", always=True)
    def set_tz(cls, v):
        """After initial validation logic, add utc as the timezone."""
        return v.replace(tzinfo=timezone.utc)


class GuidUpdate(BaseDataModel):
    """
    Serializer for updating a record.

    Formats data, so that it'll play nicely  w/ the DB.
    """

    expire: datetime = None
    name: str = None


class GuidOut(BaseDataModel):
    """Serialize output, that'll be sent to the end user properly."""

    id: str
    expire: datetime
    name: str

    @validator("expire")
    def check_expire(cls, v: Union[datetime, str]) -> str:
        """Coerce expire into being Unix Time."""
        if type(v) == str:
            v = datetime.fromisoformat(v)
        return str(int(v.replace(tzinfo=timezone.utc).timestamp()))
