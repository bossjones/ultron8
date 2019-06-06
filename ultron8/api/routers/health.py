"""Temporary router for user objects. Taken directly from FastApi Tutorial"""

from fastapi import APIRouter, HTTPException
from ultron8.api.models.health import HealthOut
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", tags=["health"], response_model=HealthOut)
async def read_health():
    content = {"status": "OK"}
    return HealthOut(**content)
