from pydantic import BaseModel
from ultron8.api.models.base import BaseDataModel


class Token(BaseDataModel):
    access_token: str
    token_type: str


class TokenPayload(BaseDataModel):
    user_id: int = None
