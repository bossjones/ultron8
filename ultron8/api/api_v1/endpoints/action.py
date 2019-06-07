"""Temporary router for Action objects. Taken directly from FastApi Tutorial"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/v1/actions/", tags=["actions"])
async def get_actions():
    return [{"username": "Foo"}, {"username": "Bar"}]
