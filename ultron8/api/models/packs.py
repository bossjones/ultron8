from datetime import datetime
import logging

from typing import Optional

from pydantic import BaseModel, Schema

from ultron8.api.models.base import BaseDataModel

# SOURCE: https://github.com/tiangolo/fastapi/issues/634
try:
    from pydantic import EmailStr
except ImportError:
    from pydantic.networks import EmailStr


log = logging.getLogger(__name__)

# from pydantic import (DSN, UUID1, UUID3, UUID4, UUID5, BaseModel, DirectoryPath, EmailStr, FilePath, NameEmail,
# NegativeFloat, NegativeInt, PositiveFloat, PositiveInt, PyObject, UrlStr, conbytes, condecimal,
# confloat, conint, constr, IPvAnyAddress, IPvAnyInterface, IPvAnyNetwork, SecretStr, SecretBytes)


# == Schema Information
#
# Table name: projects
#
#  id                        :integer          not null, primary key
#  name                      :string
#  environment_id            :integer
#  created_at                :datetime
#  updated_at                :datetime
#  rollback                  :boolean          default(TRUE)
#  deleted_at                :datetime
#  deployed_sha_for_rollback :boolean          default(TRUE)
#  last_good_build_id        :integer
#  required                  :boolean          default(TRUE), not null
#  title                     :string
#  project_group_id          :integer
#  environment_stage_id      :integer
#  unstable_allowed          :boolean          default(TRUE)
#
# Indexes
#
#  index_projects_on_deleted_at      (deleted_at)
#  index_projects_on_environment_id  (environment_id)
#

# SOURCE: https://docs.stackstorm.com/reference/packs.html
class PacksBase(BaseDataModel):
    """[summary]

    === Schema example:

    name : linux
    description : Generic Linux actions
    keywords:
      - linux
      - nmap
      - lsof
      - traceroute
      - loadavg
      - cp
      - scp
      - dig
      - netstat
      - rsync
      - vmstat
      - open ports
      - processes
      - ps
    version : 1.0.1
    python_versions:
      - "3"
    author : Jarvis
    email : info@theblacktonystark.com

    Arguments:
        BaseModel {[type]} -- [description]
    """

    # Pack reference. It can only contain letters, digits and underscores.
    ref: Optional[str] = None
    # User-friendly pack name. If this attribute contains spaces or any other special characters, then
    # the "ref" attribute must also be specified (see above).
    name: Optional[str] = None
    # User-friendly pack description.
    description: Optional[str] = None
    # Keywords which are used when searching for packs.
    # keywords: Optional[List[str]] = []  # List of strings, default to []
    keywords: Optional[str] = None
    # Pack version which must follow semver format (<major>.<minor>.<patch> e.g. 1.0.0)
    version: Optional[str] = None
    # A list of major Python versions pack is tested with and works with.
    # python_versions: Optional[List[str]] = []
    python_versions: Optional[str] = None
    # Name of the pack author.
    author: Optional[str] = None
    # Email of the pack author.
    email: Optional[EmailStr] = None

    contributors: Optional[str] = None

    class Config:
        orm_mode = True


class PacksBaseInDB(PacksBase):
    id: int = None
    uid: str = None
    created_at: datetime = None
    updated_at: datetime = None
    files: str
    path: str
    # actions: Optional[ActionInDB] = []


# Properties to receive via API on creation
class PacksCreate(PacksBaseInDB):
    # Pack reference. It can only contain letters, digits and underscores.
    ref: str
    # User-friendly pack name. If this attribute contains spaces or any other special characters, then
    # the "ref" attribute must also be specified (see above).
    name: str
    # User-friendly pack description.
    description: str
    # Keywords which are used when searching for packs.
    # keywords: List[str]
    keywords: str
    # Pack version which must follow semver format (<major>.<minor>.<patch> e.g. 1.0.0)
    # version: str
    version: str
    # A list of major Python versions pack is tested with and works with.
    # python_versions: List[str]
    python_versions: str
    # Name of the pack author.
    author: str
    # Email of the pack author.
    email: EmailStr
    # contributors
    contributors: str


# Properties to receive via API on update
class PacksUpdate(PacksBaseInDB):
    pass


# DB representation of Pack, with correctly scoped types etc
# class PacksInDB(PacksBaseInDB):


class PacksData(PacksCreate):
    pass


# smoke-tests
# if "__main__" == __name__:
# external_data = {
#     "name": "local_ps_aux",
#     "runner_type": "local-shell-cmd",
#     "description": "Run ps aux locally",
#     "enabled": True,
#     "entry_point": "",
#     "parameters": {
#         "cmd": {"immutable": True, "default": "ps aux"},
#         "sudo": {"default": False},
#     },
# }

# action = ActionBase(**external_data)

# print("----------- action ------------")
# print(action)

# print("----------- action.name ------------")
# print(f"action.name = '{action.name}''")
