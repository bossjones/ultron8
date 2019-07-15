import requests

from tests.utils.utils import random_lower_string
from ultron8.api import crud
from ultron8.api import settings
from ultron8.api.db.u_sqlite.session import db_session

# from ultron8.api.models.packs import UserCreate


# def packs_authentication_headers(server_api, email, password):
#     data = {"packsname": email, "password": password}

#     r = requests.post(
#         f"{server_api}{settings.API_V1_STR}/login/access-token", data=data
#     )
#     response = r.json()
#     auth_token = response["access_token"]
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     return headers


# def create_random_packs():
#     email = random_lower_string()
#     password = random_lower_string()
#     packs_in = UserCreate(packsname=email, email=email, password=password)
#     packs = crud.packs.create(db_session=db_session, packs_in=packs_in)
#     return packs
