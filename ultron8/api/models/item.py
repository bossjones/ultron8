from pydantic import BaseModel
from ultron8.api.models.base import BaseDataModel


# Shared properties
class ItemBase(BaseDataModel):
    title: str = None
    description: str = None

    class Config:
        orm_mode = True


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str

    class Config:
        orm_mode = True


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
