"""Helpers for config validation using voluptuous."""
from datetime import (
    timedelta,
    datetime as datetime_sys,
    time as time_sys,
    date as date_sys,
)
import os
import re
from urllib.parse import urlparse
from socket import _GLOBAL_DEFAULT_TIMEOUT
import logging
import inspect
import sys
import traceback
from typing import (
    Any,
    Union,
    TypeVar,
    Callable,
    Sequence,
    Dict,
    List,
    Iterator,
    overload,
)

from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.compat import ordereddict

from collections import OrderedDict

# import voluptuous as vol
# from voluptuous.humanize import humanize_error

LOGGER = logging.getLogger(__name__)

# if os.environ.get("MOONBEAM_CLI_DEV_MODE"):
#     from ultron8.debugger import init_debugger

#     init_debugger()

# # pylint: disable=invalid-name

# TIME_PERIOD_ERROR = "offset {} should be format 'HH:MM' or 'HH:MM:SS'"

# JSON_TYPE = Union[List, Dict, str]  # pylint: disable=invalid-name
# DICT_T = TypeVar("DICT_T", bound=Dict)  # pylint: disable=invalid-name
# # typing typevar
# T = TypeVar("T")


# # NOTE: In typical Python code, many functions that can take a list or a dict as an argument only need their argument to be somehow "list-like" or "dict-like". A specific meaning of "list-like" or "dict-like" (or something-else-like) is called a "duck type", and several duck types that are common in idiomatic Python are standardized.
# DUCK_TYPE = Union[T, Sequence[T]]  # pylint: disable=invalid-name
# LIST_TYPE = Sequence[T]

# # Adapted from:
# # https://github.com/alecthomas/voluptuous/issues/115#issuecomment-144464666
# def has_at_least_one_key(*keys: str) -> Callable:
#     """Validate that at least one key exists."""

#     def validate(obj: Dict) -> Dict:
#         """Test keys exist in dict."""
#         if not isinstance(obj, dict):
#             raise vol.Invalid("expected dictionary")

#         for k in obj.keys():
#             if k in keys:
#                 return obj
#         raise vol.Invalid("must contain one of {}.".format(", ".join(keys)))

#     return validate


# def boolean(value: Any) -> bool:
#     """Validate and coerce a boolean value."""
#     if isinstance(value, str):
#         value = value.lower()
#         if value in ("1", "true", "yes", "on", "enable"):
#             return True
#         if value in ("0", "false", "no", "off", "disable"):
#             return False
#         raise vol.Invalid("invalid boolean value {}".format(value))
#     return bool(value)


# def ensure_list(value: Union[T, Sequence[T]]) -> Sequence[T]:
#     """Wrap value in list if it is not one."""
#     if value is None:
#         return []
#     return value if isinstance(value, list) else [value]


# def enum(enumClass):
#     """Create validator for specified enum."""
#     return vol.All(vol.In(enumClass.__members__), enumClass.__getitem__)


# # time_period_dict = vol.All(
# #     dict, vol.Schema({
# #         'days': vol.Coerce(int),
# #         'hours': vol.Coerce(int),
# #         'minutes': vol.Coerce(int),
# #         'seconds': vol.Coerce(int),
# #         'milliseconds': vol.Coerce(int),
# #     }),
# #     has_at_least_one_key('days', 'hours', 'minutes',
# #                          'seconds', 'milliseconds'),
# #     lambda value: timedelta(**value))


# def string(value: Any) -> str:
#     """Coerce value to string, except for None."""
#     if value is not None:
#         return str(value)
#     raise vol.Invalid("string value is None")


# # pylint: disable=no-value-for-parameter
# def url(value: Any) -> str:
#     """Validate an URL."""
#     url_in = str(value)

#     if urlparse(url_in).scheme in ["http", "https"]:
#         return vol.Schema(vol.Url())(url_in)

#     raise vol.Invalid("invalid url")


# # Validator helpers


# def key_dependency(key, dependency):
#     """Validate that all dependencies exist for key."""

#     def validator(value):
#         """Test dependencies."""
#         if not isinstance(value, dict):
#             raise vol.Invalid("key dependencies require a dict")
#         if key in value and dependency not in value:
#             raise vol.Invalid(
#                 'dependency violation - key "{}" requires '
#                 'key "{}" to exist'.format(key, dependency)
#             )

#         return value

#     return validator


# ###################################################################################################################
# # Schemas
# ###################################################################################################################

# # <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# # Working version so far (9/24/2018)
# MOONBEAM_SERVICE_SCHEMA = vol.Schema(
#     {
#         # list of image definition names, will be used for optimization in the future to allow us to write less when building these config objects
#         vol.Optional("image_definition_names"): [str],
#         # Data used in POST /v1/provision body
#         vol.Required("payload"): vol.All(
#             [
#                 vol.Schema(
#                     {
#                         # To provision a Jenkins box, add the following blob to the provision request
#                         vol.Optional("jenkins_build_configurations"): vol.All(
#                             [
#                                 vol.Schema(
#                                     {
#                                         vol.Optional("build_url"): string,
#                                         vol.Optional("build_type"): vol.Schema(
#                                             vol.Any(
#                                                 "jenkins",
#                                                 "lambda",
#                                                 msg="Sorry, 'jenkins' and 'lambda' are mutually exclusive for option 'build_type' in 'jenkins_build_configurations'. Pick one",
#                                             )
#                                         ),
#                                         vol.Optional("display_url"): string,
#                                         vol.Optional("name"): string,
#                                         vol.Optional("password"): string,
#                                         vol.Optional("username"): string,
#                                     }
#                                 )
#                             ]
#                         ),
#                         # Github service organization
#                         vol.Optional("organizations"): vol.All(
#                             [
#                                 vol.Schema(
#                                     {
#                                         vol.Optional("login_allowed"): boolean,
#                                         vol.Optional("name"): string,
#                                     },
#                                     extra=vol.PREVENT_EXTRA,
#                                 )
#                             ]
#                         ),
#                         # Github service organization
#                         vol.Optional("services"): vol.All(
#                             [
#                                 vol.Schema(
#                                     {
#                                         # Service Environments
#                                         vol.Required("environments"): vol.All(
#                                             [
#                                                 vol.Schema(
#                                                     {
#                                                         vol.Optional(
#                                                             "checklist_items"
#                                                         ): vol.All(
#                                                             [
#                                                                 {
#                                                                     vol.Optional(
#                                                                         "item"
#                                                                     ): string,
#                                                                     vol.Optional(
#                                                                         "item_type"
#                                                                     ): string,
#                                                                     vol.Optional(
#                                                                         "required"
#                                                                     ): boolean,
#                                                                 }
#                                                             ]
#                                                         ),
#                                                         vol.Optional(
#                                                             "environment_stages"
#                                                         ): vol.All(
#                                                             [
#                                                                 vol.Schema(
#                                                                     {
#                                                                         vol.Optional(
#                                                                             "name"
#                                                                         ): string,
#                                                                         vol.Optional(
#                                                                             "step"
#                                                                         ): int,
#                                                                         vol.Optional(
#                                                                             "project_group"
#                                                                         ): vol.Schema(
#                                                                             {
#                                                                                 vol.Optional(
#                                                                                     "name"
#                                                                                 ): string
#                                                                             }
#                                                                         ),
#                                                                     }
#                                                                 )
#                                                             ]
#                                                         ),
#                                                         vol.Optional("name"): string,
#                                                         vol.Optional(
#                                                             "production"
#                                                         ): boolean,
#                                                         vol.Optional(
#                                                             "projects"
#                                                         ): vol.All(
#                                                             [
#                                                                 vol.Schema(
#                                                                     {
#                                                                         vol.Optional(
#                                                                             "build_params"
#                                                                         ): vol.All(
#                                                                             [
#                                                                                 vol.Schema(
#                                                                                     {
#                                                                                         vol.Optional(
#                                                                                             "name"
#                                                                                         ): string,
#                                                                                         vol.Optional(
#                                                                                             "param_type"
#                                                                                         ): string,
#                                                                                         vol.Optional(
#                                                                                             "default"
#                                                                                         ): string,
#                                                                                         vol.Optional(
#                                                                                             "hidden"
#                                                                                         ): boolean,
#                                                                                         vol.Optional(
#                                                                                             "end_value"
#                                                                                         ): string,  # or empty
#                                                                                         vol.Optional(
#                                                                                             "description"
#                                                                                         ): string,
#                                                                                     }
#                                                                                 )
#                                                                             ]
#                                                                         ),
#                                                                         vol.Optional(
#                                                                             "build_type"
#                                                                         ): vol.Schema(
#                                                                             vol.Any(
#                                                                                 "jenkins",
#                                                                                 "lambda",
#                                                                                 msg="Sorry, 'jenkins' and 'lambda' are mutually exclusive for option 'build_type'. Pick one",
#                                                                             )
#                                                                         ),
#                                                                         vol.Optional(
#                                                                             "deploy_token"
#                                                                         ): boolean,
#                                                                         vol.Exclusive(
#                                                                             "jenkins",
#                                                                             "lambda",
#                                                                             msg="Sorry, 'jenkins' and 'lambda' are mutually exclusive. Pick one",
#                                                                         ): string,
#                                                                         # vol.Optional("jenkins"): string,
#                                                                         # vol.Optional("lambda"): string,
#                                                                         vol.Optional(
#                                                                             "name"
#                                                                         ): string,
#                                                                         vol.Optional(
#                                                                             "rollback"
#                                                                         ): boolean,
#                                                                         vol.Optional(
#                                                                             "stage"
#                                                                         ): string,
#                                                                         vol.Optional(
#                                                                             "unstable_allowed"
#                                                                         ): boolean,
#                                                                         vol.Optional(
#                                                                             "project_group"
#                                                                         ): string,
#                                                                     },
#                                                                     has_at_least_one_key(
#                                                                         "jenkins",
#                                                                         "lambda",
#                                                                     ),
#                                                                     extra=vol.ALLOW_EXTRA,
#                                                                 )
#                                                             ]
#                                                         ),
#                                                         vol.Optional(
#                                                             "single_rollback_allowed"
#                                                         ): boolean,
#                                                         vol.Optional("tier"): int,
#                                                     }
#                                                 )  # end - environment_stages
#                                             ]  # end - environments_stages (list)
#                                         ),  # end - Service Environments
#                                         vol.Required("name"): string,
#                                         vol.Required("product"): string,
#                                         # service repository object
#                                         vol.Required("repository"): vol.Schema(
#                                             {
#                                                 vol.Optional(
#                                                     "github_webhook_secrets"
#                                                 ): vol.All(
#                                                     [
#                                                         vol.Schema(
#                                                             {
#                                                                 vol.Optional(
#                                                                     "token"
#                                                                 ): string,
#                                                                 vol.Optional(
#                                                                     "webhook_type"
#                                                                 ): string,
#                                                             }
#                                                         )
#                                                     ]
#                                                 ),
#                                                 vol.Optional("min_approvers"): int,
#                                                 vol.Optional(
#                                                     "multi_merge_allowed"
#                                                 ): boolean,
#                                                 vol.Optional("name"): string,
#                                                 vol.Optional("owner"): string,
#                                             }
#                                         ),
#                                         vol.Optional("slack_configs"): vol.All(
#                                             [
#                                                 vol.Schema(
#                                                     {
#                                                         vol.Optional("channel"): string,
#                                                         vol.Optional("team"): string,
#                                                         vol.Optional(
#                                                             "username"
#                                                         ): string,
#                                                     }
#                                                 )
#                                             ]
#                                         ),
#                                     }
#                                 )
#                             ]
#                         ),
#                         # slack_teams
#                         vol.Optional("slack_teams"): vol.All(
#                             [
#                                 vol.Schema(
#                                     {
#                                         vol.Optional("id"): int,
#                                         vol.Optional("name"): string,
#                                     }
#                                 )
#                             ]
#                         ),
#                     }
#                 )
#             ]
#         ),
#     }
# )


# def run_moonbeam_service_schema_validation(config):
#     """Function responsible for validating Moonbeam Service Config Schema"""
#     schema = None
#     try:
#         schema = MOONBEAM_SERVICE_SCHEMA(config)  # type: ignore
#     except vol.Invalid as err:
#         LOGGER.warning(
#             "[IMPORTING DEBUGGING FUNCTIONS]: from ultron8.debugger import ( debug_dump, dump_all, dump_color, dump_dict, dump_dir, dump_magic, dump_vars, get_pprint) "
#         )
#         from ultron8 import debugger
#         from ultron8.debugger import (
#             debug_dump,
#             dump_all,
#             dump_color,
#             dump_dict,
#             dump_dir,
#             dump_magic,
#             dump_vars,
#             get_pprint,
#         )

#         LOGGER.error("Error Class: {}".format(str(err.__class__)))
#         output = "[{}] {}: {}".format("UNEXPECTED", type(err).__name__, err)
#         LOGGER.warning(output)
#         LOGGER.error(
#             "Invalid configuration for multi-factor module %s: %s",
#             "provision_schema",
#             humanize_error(config, err),
#         )
#         exc_type, exc_value, exc_traceback = sys.exc_info()
#         LOGGER.error("exc_type: {}".format(exc_type))
#         LOGGER.error("exc_value: {}".format(exc_value))
#         traceback.print_tb(exc_traceback)
#         # import pdb;pdb.set_trace()
#         raise
#     return schema


# # NOTE: Debugging purposes, figure out subclass paths
# # SOURCE: https://stackoverflow.com/questions/3862310/how-to-find-all-the-subclasses-of-a-class-given-its-name
# def all_subclasses(cls):
#     return set(cls.__subclasses__()).union(
#         [s for c in cls.__subclasses__() for s in all_subclasses(c)]
#     )


# # smoke-tests
# if __name__ == "__main__":
#     import logging
#     import ultron8
#     from ultron8.loggers import setup_logger
#     from ultron8.config import Config, MoonbeamServiceConfig
#     from ultron8.yaml import yaml
#     import json as jsonlib
#     import ultron8.validation as validationlib

#     setup_logger()

#     # load moonbeam service config object
#     m_cfg = MoonbeamServiceConfig()
#     m_cfg.load_service("flask-ethos-test", "v1")

#     # Repopulate payload with secret values ( instead of 'REDACTED' )
#     m_cfg.update_with_secrets("moonbeam-ethos-dev")

#     print("m_cfg.service_definition TYPE = {}".format(type(m_cfg.service_definition)))

#     print("BEFORE - m_cfg.service_definition str = {}".format(m_cfg.service_definition))

#     from ultron8 import debugger
#     from ultron8.debugger import (
#         debug_dump,
#         dump_all,
#         dump_color,
#         dump_dict,
#         dump_dir,
#         dump_magic,
#         dump_vars,
#         get_pprint,
#     )

#     validated_service_definition = validationlib.run_moonbeam_service_schema_validation(
#         m_cfg.service_definition
#     )

#     print("Ran validation of service definition successfully")

#     print(jsonlib.dumps(validated_service_definition, indent=4))

#     print(
#         "AFTER - m_cfg.service_definition str = {}".format(validated_service_definition)
#     )
