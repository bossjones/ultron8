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
    salt: Optional[str] = None
    hashed_password: str

    class Config:
        orm_mode = True

    # TODO: Enable this so we can securely story password salt+hash. See https://github.com/bossjones/ultron8/issues/63
    # def check_password(self, password: str) -> bool:
    #     return security.verify_password(self.salt + password, self.hashed_password)

    # def change_password(self, password: str) -> None:
    #     self.salt = security.generate_salt()
    #     self.hashed_password = security.get_password_hash(self.salt + password)
