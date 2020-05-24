from pydantic import BaseModel

from ultron8.api.models.base import BaseDataModel


class Msg(BaseDataModel):
    msg: str

    class Config:
        orm_mode = True
