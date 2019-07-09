"""Temporary router for user objects. Taken directly from FastApi Tutorial"""
from fastapi import APIRouter
from fastapi import HTTPException

router = APIRouter()


@router.get("/")
async def read_home():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]
