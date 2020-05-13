import requests

from tests.utils.utils import random_lower_string, random_email
from ultron8.api import crud
from ultron8.api import settings
from ultron8.api.db.u_sqlite.session import db_session
from ultron8.api.models.user import UserCreate, UserUpdate

from sqlalchemy.orm import Session
from typing import Dict
from ultron8.api.db_models.user import User
from typing import Optional
from starlette.testclient import TestClient


def user_authentication_headers(
    server_api: str, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/login/access-token", data=data
    )
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


# SOURCE: https://github.com/KyriakosFrang/sandbox/blob/c98be415c6b7e01768c4ab2d086e147cdc86757c/fastAPI_sandbox/backend/app/app/tests/utils/user.py
def user_authentication_headers2(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    """Does basically the same as user_authentication_headers() only this time it uses the starlette TestClient

    Arguments:
        client {TestClient} -- [description]
        email {str} -- [description]
        password {str} -- [description]

    Returns:
        Dict[str, str] -- [description]
    """
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


# def create_random_user(db_session: Session) -> User:
def create_random_user() -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = crud.user.create(db_session=db_session, user_in=user_in)
    return user


def authentication_token_from_email(
    *, client: TestClient, email: str, db_session: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = crud.user.get_by_email(db_session, email=email)
    if not user:
        user_in_create = UserCreate(username=email, email=email, password=password)
        user = crud.user.create(db_session, user_in=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        user = crud.user.update(db_session, user=user, user_in=user_in_update)

    return user_authentication_headers2(client=client, email=email, password=password)
