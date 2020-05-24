# SOURCE: # SOURCE: https://github.com/bergran/fast-api-project-template
from fastapi import Depends, HTTPException
from jose import jwt
from starlette import status
from starlette.requests import Request

# from apps.token.depends.get_jwt import get_jwt
from ultron8.api import settings
from ultron8.api.depends.get_jwt import get_jwt
from ultron8.exceptions.jwt import InvalidSignatureError


def get_token_decoded(request: Request, jwt_token: str = Depends(get_jwt)) -> str:
    # config = request.state.config
    """it will check if jwt is valid and return payload. If token is expirated it will raise HTTPException and response with status code 400.

    Arguments:
        request {Request} -- [description]

    Keyword Arguments:
        jwt_token {str} -- [description] (default: {Depends(get_jwt)})

    Raises:
        HTTPException: [description]
        HTTPException: [description]

    Returns:
        str -- [description]
    """

    try:
        token = jwt.decode(jwt_token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    except InvalidSignatureError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))

    return token
