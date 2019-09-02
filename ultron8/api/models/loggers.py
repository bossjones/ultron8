# SOURCE: https://blog.bartab.fr/fastapi-logging-on-the-fly/
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class LoggerPatch(BaseModel):
    name: str
    level: str


class LoggerModel(BaseModel):
    name: str
    level: Optional[int]
    children: Optional[List["LoggerModel"]] = None


LoggerModel.update_forward_refs()
