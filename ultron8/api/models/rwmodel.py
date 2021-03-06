# pylint: disable=E0611
# NOTE: fixes [pylint] No name 'BaseModel' in module 'pydantic'
# SOURCE: https://github.com/nokia-wroclaw/innovativeproject-sudoku/issues/39

import datetime

from pydantic import BaseConfig, BaseModel


def convert_datetime_to_realworld(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )


class RWModel(BaseModel):
    class Config(BaseConfig):
        # whether an aliased field may be populated by its name as given by the model attribute, as well as the alias (default: False)
        allow_population_by_field_name = True
        # a dict used to customise the way types are encoded to JSON; see https://pydantic-docs.helpmanual.io/usage/exporting_models/#modeljson
        json_encoders = {datetime.datetime: convert_datetime_to_realworld}
        # If data source field names do not match your code style (e. g. CamelCase fields), you can automatically generate aliases using alias_generator
        alias_generator = convert_field_to_camel_case
