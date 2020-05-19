from typing import Optional

from pydantic import BaseModel
from ultron8.api.models.base import BaseDataModel


# Shared properties
class UserBase(BaseDataModel):
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: Optional[str] = None

    class Config:
        orm_mode = True


class UserBaseInDB(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class UserCreate(UserBaseInDB):
    email: str
    password: str

    class Config:
        orm_mode = True


# Properties to receive via API on update
class UserUpdate(UserBaseInDB):
    password: Optional[str] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserBaseInDB):
    pass


# Additional properties stored in DB
class UserInDB(UserBaseInDB):
    hashed_password: str

    class Config:
        orm_mode = True
