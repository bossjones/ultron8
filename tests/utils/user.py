import requests

from tests.utils.utils import random_lower_string
from ultron8.api import crud
from ultron8.api import settings
from ultron8.api.db.u_sqlite.session import db_session
from ultron8.api.models.user import UserCreate


from typing import Dict
from ultron8.api.db_models.user import User
from typing import Optional


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


def create_random_user() -> User:
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = crud.user.create(db_session=db_session, user_in=user_in)
    return user
