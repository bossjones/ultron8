from typing import Optional
from pydantic import BaseModel

# from ultron8.api.models.base import BaseDataModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    # user_id: int = None
    sub: Optional[int] = None
