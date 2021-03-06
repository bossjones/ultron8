"""
Data Models for all things having to do with Rule.
"""
from datetime import datetime

from pydantic import BaseModel, EmailStr, Schema

from ultron8.api.models.base import BaseDataModel


class RuleTypeDB(BaseDataModel):
    enabled: bool
    parameters: dict = {}

    class Config:
        orm_mode = True


class RuleTypeSpecDB(BaseDataModel):
    ref: str
    parameters: dict = {}

    class Config:
        orm_mode = True


class ActionExecutionSpecDB(BaseDataModel):
    ref: str
    parameters: dict = {}

    class Config:
        orm_mode = True


# class _ClassPropertyDescriptor:
#     __slots__ = ('getter', )

#     def __init__(self, getter):
#         self.getter = getter

#     def __get__(self, instance, owner):
#         return self.getter(owner)

# classproperty = _ClassPropertyDescriptor


class RuleBase(BaseDataModel):
    """Rule Data Model.
    =======================
    name: on_hello_event1
    pack: hello_st2
    description: Sample rule firing on hello_st2.event1.
    enabled: true
    trigger:
        type: hello_st2.event1
    action:
        ref: hello_st2.greet
        parameters:
            greeting: Yo
    """

    name: str
    pack: str
    description: str
    enabled: bool = True
    trigger: dict = {}
    action: dict = {}

    class Config:
        orm_mode = True
        # keep_untouched = (classproperty, )

    # @classproperty
    # def class_name(cls) -> str:
    #     return cls.__name__


## SOURCE: https://docs.stackstorm.com/rules.html
## NOTE: Example of a time based trigger
## trigger:
##  type: "core.st2.IntervalTimer"
##   parameters:
##       unit: "seconds"
##       delta: 30


class RuleBaseDB(RuleBase):
    id: int
    ref: str
    pack: str
    type: RuleTypeSpecDB = ...
    trigger: str
    criteria: dict = {}
    action: ActionExecutionSpecDB
    # Contextual info on the rule
    context: dict = {}
    enabled: bool
    created_at: datetime = None
    updated_at: datetime = None


if "__main__" == __name__:
    # Self-referencing Model
    # RuleModel.update_forward_refs()
    external_data = {
        "class_name": "FileWatchRule",
        "enabled": True,
        "entry_point": "file_watch_rule.py",
        "description": "Rule which monitors files for new lines",
        "trigger_types": [
            {
                "name": "file_watch.line",
                "pack": "linux",
                "description": "Trigger which indicates a new line has been detected",
                "parameters_schema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "description": "Path to the file to monitor",
                            "type": "string",
                            "required": True,
                        }
                    },
                    "additionalProperties": False,
                },
                "payload_schema": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string"},
                        "file_name": {"type": "string"},
                        "line": {"type": "string"},
                    },
                },
            }
        ],
    }

    rule = RuleBase(**external_data)
    print(rule)

    # print(rule.class_name)
