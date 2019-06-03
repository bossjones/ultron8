# ---------------------------------------------
# EXAMPLE YAML
# ---------------------------------------------
# ---
# name : linux
# description : Generic Linux actions
# keywords:
#   - linux
#   - nmap
#   - lsof
#   - traceroute
#   - loadavg
#   - cp
#   - scp
#   - dig
#   - netstat
#   - rsync
#   - vmstat
#   - open ports
#   - processes
#   - ps
# version : 1.0.1
# python_versions:
#   - "3"
# author : Jarvis
# email : info@theblacktonystark.com

from typing import List
from enum import Enum
from pydantic import BaseModel, Schema, EmailStr
from datetime import datetime

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


class PacksModel(BaseModel):
    id: int
    name: str
    description: str = None
    keywords: List[str] = []  # List of strings, default to []
    version: float
    python_versions: List[str] = []
    author: str = None
    email: EmailStr = None
    created_at: datetime = None
    updated_at: datetime = None
    deleted_at: datetime = None


# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: bool = None


# print(MainModel.schema())
# # > {
# #       'type': 'object',
# #       'title': 'Main',
# #       'properties': {
# #           'foo_bar': {
# #           ...
# print(MainModel.schema_json(indent=2))

# print(m.dict())
