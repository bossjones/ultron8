from pydantic import BaseModel


class Msg(BaseModel):
    msg: str

    class Config:
        orm_mode = True
