# SOURCE: https://github.com/bergran/fast-api-project-template
import re

from fastapi import Header, HTTPException
from starlette import status
from starlette.requests import Request

# from apps.token.constants.jwt import JWT_REGEX
from ultron8.constants.jwt import JWT_REGEX
from ultron8.api import settings

# it will regex always Authorization header with the header config that you set it or default JWT. If header does not exist or has not ^{header} [A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$ format then will raise HTTPException and response with status code 400.


def get_jwt(
    request: Request, authorization: str = Header("", alias="Authorization")
) -> str:
    """Uses regex to test existence of header in specified format. If the correct header does not exist, it will raise HTTPException and response with status code 400.

    Arguments:
        request {Request} -- [description]

    Keyword Arguments:
        authorization {str} -- [description] (default: {Header('', alias='Authorization')})

    Raises:
        HTTPException: [description]

    Returns:
        str -- [description]
    """
    # config = request.state.config

    regex = JWT_REGEX.format(settings.JWT_AUTH_HEADER_PREFIX)

    if not re.match(regex, authorization):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization has wrong format",
        )

    return authorization.split(" ")[-1]
