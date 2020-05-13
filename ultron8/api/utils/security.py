import logging

# import jwt
from jose import jwt
from pydantic import ValidationError
from fastapi import Depends
from fastapi import HTTPException

# from fastapi import Security
from fastapi.security import OAuth2PasswordBearer

# TODO: Look into security scopes https://github.com/tiangolo/fastapi/issues/840 # from fastapi.security import OAuth2AuthorizationCodeBearer, SecurityScopes
# from jwt import PyJWTError
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

from ultron8.api import crud
from ultron8.api import settings
from ultron8.api.core.jwt import ALGORITHM
from ultron8.api.db_models.user import User
from ultron8.api.models.token import TokenPayload
from ultron8.api.utils.db import get_db

logger = logging.getLogger(__name__)

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/v1/login/access-token")


# def get_current_user(
#     db: Session = Depends(get_db), token: str = Security(reusable_oauth2)
# ):
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
#         token_data = TokenPayload(**payload)
#     except PyJWTError:
#         raise HTTPException(
#             status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
#         )
#     user = crud.user.get(db, user_id=token_data.user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials",
        )
    # user = crud.user.get(db, id=token_data.sub)
    user = crud.user.get(db, user_id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
