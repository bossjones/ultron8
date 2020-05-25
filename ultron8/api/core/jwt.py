from datetime import datetime, timedelta
import logging

from typing import Any, Union

from jose import jwt

from ultron8.api import settings

# import jwt


ALGORITHM = "HS256"
access_token_jwt_subject = "access"

logger = logging.getLogger(__name__)


# def create_access_token(*, data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     logger.debug("[create_access_token] to_encode data = {}".format(to_encode))
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
#     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
