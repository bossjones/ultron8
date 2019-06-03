from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from enum import Enum
from pydantic import BaseModel, Schema, EmailStr
from datetime import datetime

# == Schema Information
# ---
# name: "check_loadavg"
# runner_type: "remote-shell-script"
# description: "Check CPU Load Average on a Host"
# enabled: true
# entry_point: "checks/check_loadavg.py"
# parameters:
#   period:
#     enum:
#       - "1"
#       - "5"
#       - "15"
#       - "all"
#     type: "string"
#     description: "Time period for load avg: 1,5,15 minutes, or 'all'"
#     default: "all"
#     position: 0


class ActionsModel(BaseModel):
    # id: int
    name: str
    runner_type: str
    description: str = None
    enabled: bool
    entry_point: str  # eg. "checks/check_loadavg.py"
    parameters: Dict[str, float, int, bool, List, dict] = None
    tags: List[str] = []
    created_at: datetime = None
    updated_at: datetime = None
    deleted_at: datetime = None
