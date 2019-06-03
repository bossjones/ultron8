"""Temporary router for user objects. Taken directly from FastApi Tutorial"""
from ultron8 import __version__

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/version")
def read_version():
    cur_version = f"{__version__}"
    return [{"version": cur_version}]
