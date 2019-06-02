"""Temporary router for user objects. Taken directly from FastApi Tutorial"""

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
def read_home():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]
