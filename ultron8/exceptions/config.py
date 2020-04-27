# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""All Config exceptions."""

import yaml

YAML_TAB_PROBLEM = "found character '\\t' that cannot start any token"

# configuration errors
class ConfigError(Exception):
    """Base class for exceptions raised when querying a configuration.
    """


class ConfigNotFoundError(ConfigError):
    """A requested value could not be found in the configuration trees.
    """


class ConfigValueError(ConfigError):
    """The value in the configuration is illegal."""


class ConfigTypeError(ConfigValueError):
    """The value in the configuration did not match the expected type.
    """


class ConfigTemplateError(ConfigError):
    """Base class for exceptions raised because of an invalid template.
    """


class ConfigReadError(ConfigError):
    """A configuration file could not be read."""

    def __init__(self, filename, reason=None):
        self.filename = filename
        self.reason = reason

        message = "file {0} could not be read".format(filename)
        if (
            isinstance(reason, yaml.scanner.ScannerError)
            and reason.problem == YAML_TAB_PROBLEM
        ):
            # Special-case error message for tab indentation in YAML markup.
            message += ": found tab character at line {0}, column {1}".format(
                reason.problem_mark.line + 1, reason.problem_mark.column + 1,
            )
        elif reason:
            # Generic error message uses exception's message.
            message += ": {0}".format(reason)

        super().__init__(message)
