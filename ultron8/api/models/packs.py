import logging
from datetime import datetime
from enum import Enum
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Schema

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
class PacksBase(BaseModel):
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
    keywords: Optional[List[str]] = []  # List of strings, default to []
    # Pack version which must follow semver format (<major>.<minor>.<patch> e.g. 1.0.0)
    version: Optional[float] = None
    # A list of major Python versions pack is tested with and works with.
    python_versions: Optional[List[str]] = []
    # Name of the pack author.
    author: Optional[str] = None
    # Email of the pack author.
    email: Optional[EmailStr] = None
    # contributors


class PacksBaseInDB(PacksBase):
    id: int = None
    created_at: datetime = None
    updated_at: datetime = None
    # deleted_at: datetime = None


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
    keywords: List[str]
    # Pack version which must follow semver format (<major>.<minor>.<patch> e.g. 1.0.0)
    version: float
    # A list of major Python versions pack is tested with and works with.
    python_versions: List[str]
    # Name of the pack author.
    author: str
    # Email of the pack author.
    email: EmailStr
    # contributors


# Properties to receive via API on update
class PacksUpdate(PacksBaseInDB):
    # Pack reference. It can only contain letters, digits and underscores.
    ref: str
    # User-friendly pack name. If this attribute contains spaces or any other special characters, then
    # the "ref" attribute must also be specified (see above).
    name: str
    # User-friendly pack description.
    description: str
    # Keywords which are used when searching for packs.
    keywords: List[str]
    # Pack version which must follow semver format (<major>.<minor>.<patch> e.g. 1.0.0)
    version: float
    # A list of major Python versions pack is tested with and works with.
    python_versions: List[str]
    # Name of the pack author.
    author: str
    # Email of the pack author.
    email: EmailStr
    # contributors


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
