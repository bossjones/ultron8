"""Temporary router for user objects. Taken directly from FastApi Tutorial"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/v1/users/", tags=["users"])
def read_users():
    return [{"username": "Foo"}, {"username": "Bar"}]


@router.get("/v1/users/me", tags=["users"])
def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/v1/users/{username}", tags=["users"])
def read_user(username: str):
    return {"username": username}
