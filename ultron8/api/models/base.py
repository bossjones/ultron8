import logging
from typing import Optional
from pydantic import BaseModel as PydanticBaseModel

log = logging.getLogger(__name__)


class BaseDataModel(PydanticBaseModel):
    # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
    # This way, instead of only trying to get the id value from a dict, as in:
    # id = data["id"]
    # it will also try to get it from an attribute, as in:
    # id = data.id
    # SOURCE: https://fastapi.tiangolo.com/tutorial/sql-databases/
    class Config:
        orm_mode = True
