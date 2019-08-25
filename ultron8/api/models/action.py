import logging
from datetime import datetime
from enum import Enum
from enum import IntEnum
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import Union

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Schema

from ultron8.api.models.base import BaseDataModel

# from ultron8.api.models.packs import

log = logging.getLogger(__name__)


class RunnerTypeModel(str, Enum):
    # This is the local runner. This runner executes a Linux command on the host where StackStorm is running.
    local_shell_cmd = "local-shell-cmd"
    # This is the local runner. Actions are implemented as scripts. They are executed on the hosts where StackStorm is running.
    local_shell_script = "local-shell-script"
    # This is a remote runner. This runner executes a Linux command on one or more remote hosts provided by the user.
    remote_shell_cmd = "remote-shell-cmd"
    # This is a remote runner. Actions are implemented as scripts. They run on one or more remote hosts provided by the user.
    remote_shell_script = "remote-shell-script"
    #  This is a Python runner. Actions are implemented as Python classes with a run() method. They run locally on the same machine where StackStorm components are running. The return value from the action run() method is either a tuple of success status flag and the result object respectively or it is just the result object. For more information, please refer to the Action Runners section in the documentation.
    python_script = "python-script"
    # HTTP client which performs HTTP requests for running HTTP actions.
    http_request = "http-request"
    #  This runner supports executing simple linear work-flows. For more information, please refer to the Workflows and ActionChain documentation.
    action_chain = "action-chain"
    # This runner provides the core logic of the Inquiries feature.
    inquirer = "inquirer"


class ActionBase(BaseDataModel):
    # Pack reference. It can only contain letters, digits and underscores.
    name: Optional[str] = None
    ref: Optional[str] = None
    packs_name: Optional[str] = None
    runner_type: Optional[RunnerTypeModel] = None
    description: Optional[str] = None
    enabled: Optional[bool] = True
    entry_point: Optional[str] = None
    # pack: Optional[str] = None
    parameters: Optional[dict] = {}
    # output_Schema : Optional[Optional[str]
    # notify : Optional[Optional[str]
    tags: Optional[List[str]] = []

    class Config:
        orm_mode = True


class ActionBaseInDB(ActionBase):
    """Data Object describing Actions

    == Schema Information

    name: "check_loadavg"
    runner_type: "remote-shell-script"
    description: "Check CPU Load Average on a Host"
    enabled: true
    entry_point: "checks/check_loadavg.py"
    parameters:
      period:
        enum:
          - "1"
          - "5"
          - "15"
          - "all"
        type: "string"
        description: "Time period for load avg: 1,5,15 minutes, or 'all'"
        default: "all"
        position: 0

    Arguments:
        ActionBaseInDB {[type]} -- [description]
    """

    id: int = None
    uid: str = None
    metadata_file: Optional[str] = None
    created_at: datetime = None
    updated_at: datetime = None


class ActionCreate(ActionBaseInDB):
    # ref: str
    ref: Optional[str] = None
    name: str
    runner_type: RunnerTypeModel
    description: str = ""
    enabled: bool = True
    entry_point: str = ""
    # pack: str
    parameters: dict = {}
    # output_Schema :Optional[str]
    # notify :Optional[str]
    tags: List[str] = []
    # packs_name: Optional[str] = None


# Properties to receive via API on update
class ActionUpdate(ActionBaseInDB):
    pass


# smoke-tests
if "__main__" == __name__:
    external_data = {
        "name": "local_ps_aux",
        "runner_type": "local-shell-cmd",
        "description": "Run ps aux locally",
        "enabled": True,
        "entry_point": "",
        "parameters": {
            "cmd": {"immutable": True, "default": "ps aux"},
            "sudo": {"default": False},
        },
    }

    action = ActionBase(**external_data)

    print("----------- action ------------")
    print(action)

    print("----------- action.name ------------")
    print(f"action.name = '{action.name}''")
