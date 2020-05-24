import requests

from tests.utils.utils import random_lower_string, random_email
from ultron8.api import crud
from ultron8.api import settings

from ultron8.api.models.user import UserCreate, UserUpdate

from sqlalchemy.orm import Session
from typing import Dict
from ultron8.api.db_models.user import User
from typing import Optional
from starlette.testclient import TestClient
import factory

import random
import string
from sqlalchemy.orm.session import Session


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
def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = crud.user.create(db_session=db, user_in=user_in)
    return user


def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = crud.user.get_by_email(db, email=email)
    if not user:
        user_in_create = UserCreate(username=email, email=email, password=password)
        user = crud.user.create(db, user_in=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        user = crud.user.update(db, user=user, user_in=user_in_update)

    return user_authentication_headers2(client=client, email=email, password=password)


# def randomStringwithDigitsAndSymbols(stringLength=10):
#     """Generate a random password string with Special characters, letters, and digits.

#     Keyword Arguments:
#         stringLength {int} -- [description] (default: {10})

#     Returns:
#         [type] -- [description]
#     """
#     password_characters = string.ascii_letters + string.digits + string.punctuation
#     return ''.join(random.choice(password_characters) for i in range(stringLength))

# def random_full_name(male_or_female="male"):
#     if male_or_female == "male":
#         first_name = factory.Faker('first_name_male')
#         last_name = factory.Faker('last_name_male')
#     else:
#         first_name = factory.Faker('first_name_female')
#         last_name = factory.Faker('last_name_female')

#     return first_name.generate(), last_name.generate()

# # class FullNameFactory(factory.Factory):


# class RandomUserFactory(factory.Factory):
#     class Meta:
#         model = UserCreate

#     full_name = factory.Faker("name_male")
#     is_active = True
#     is_superuser = False
#     email = factory.Faker("free_email")
#     password =  factory.Faker("password")


# def _MakeRandomNormalUserFactory():
#     _first_name, _last_name = random_full_name()
#     _email = "{}.{}@example.org".format(_first_name, _last_name)
#     _full_name = "{} {}".format(_first_name, _last_name)
#     _password = randomStringwithDigitsAndSymbols()

#     return RandomUserFactory(
#         full_name=_full_name,
#         is_active=True,
#         is_superuser=False,
#         email=_email,
#         password=_password
#     )
