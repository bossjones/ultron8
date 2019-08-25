import logging
from typing import Optional
from pydantic import BaseModel as PydanticBaseModel

log = logging.getLogger(__name__)


class BaseDataModel(PydanticBaseModel):
    class Config:
        orm_mode = True
