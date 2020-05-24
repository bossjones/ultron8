# Copyright 2015, Adrian Sampson.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

"""Worry-free YAML configuration files.
"""

from __future__ import annotations

from collections import ChainMap, OrderedDict, abc
from copy import deepcopy
import logging
import os
from pathlib import Path
import platform
import re

from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Type, Union

# from ultron8.config import ConfigDict
# from ultron8.config.smart import Configuration
import pkg_resources
import yaml
from yaml.nodes import MappingNode, ScalarNode

from ultron8.exceptions.config import (
    YAML_TAB_PROBLEM,
    ConfigError,
    ConfigNotFoundError,
    ConfigReadError,
    ConfigTemplateError,
    ConfigTypeError,
    ConfigValueError,
)

# from devtest.core import exceptions


logger = logging.getLogger(__name__)


# UNIX_DIR_VAR = 'XDG_CONFIG_HOME'
UNIX_DIR_FALLBACK = "~/.config"
# UNIX_DIR_FALLBACK = '~/.ultron8'
MAC_DIR = "~/Library/Application Support"
WINDOWS_DIR_VAR = "APPDATA"
WINDOWS_DIR_FALLBACK = r"~\AppData\Roaming"

# CONFIG_FILENAME = 'config.yaml'
CONFIG_FILENAME = "smart.yaml"
DEFAULT_FILENAME = "smart_default.yaml"
ROOT_NAME = "root"

REDACTED_TOMBSTONE = "REDACTED"

UNIX_SYSTEM_DIR = "/etc/ultron8"


def iter_first(sequence: Iterator[Any]) -> Any:
    """Get the first element from an iterable or raise a ValueError if
    the iterator generates no values.
    """
    it = iter(sequence)
    try:
        return next(it)
    except StopIteration:
        raise ValueError()


# class ConfigReadError(ConfigError):
#     """A configuration file could not be read."""

#     def __init__(self, filename, reason=None):
#         self.filename = filename
#         self.reason = reason

#         message = "file {0} could not be read".format(filename)
#         if (
#             isinstance(reason, yaml.scanner.ScannerError)
#             and reason.problem == YAML_TAB_PROBLEM
#         ):
#             # Special-case error message for tab indentation in YAML markup.
#             message += ": found tab character at line {0}, column {1}".format(
#                 reason.problem_mark.line + 1, reason.problem_mark.column + 1,
#             )
#         elif reason:
#             # Generic error message uses exception's message.
#             message += ": {0}".format(reason)

#         super().__init__(message)


# Views and sources.


class ConfigSource(dict):
    """A dictionary augmented with metadata about the source of the
    configuration.
    """

    def __init__(
        self,
        value: Any,
        filename: Optional[Union[int, str]] = None,
        default: bool = False,
    ) -> None:
        super().__init__(value)
        if filename is not None and not isinstance(filename, str):
            raise TypeError("filename must be a string or None")
        self.filename = filename
        self.default = default

    def __repr__(self) -> str:
        return "ConfigSource({0}, {1}, {2})".format(
            super().__repr__(), repr(self.filename), repr(self.default)
        )

    @classmethod
    def of(
        self, value: Union[str, Dict[str, str], ConfigSource, Dict[int, bool]]
    ) -> ConfigSource:
        """Given either a dictionary or a `ConfigSource` object, return
        a `ConfigSource` object. This lets a function accept either type
        of object as an argument.
        """
        if isinstance(value, ConfigSource):
            return value
        elif isinstance(value, dict):
            return ConfigSource(value)
        else:
            raise TypeError("source value must be a dict")


class ConfigView(object):
    """A configuration "view" is a query into a program's configuration
    data. A view represents a hypothetical location in the configuration
    tree; to extract the data from the location, a client typically
    calls the ``view.get()`` method. The client can access children in
    the tree (subviews) by subscripting the parent view (i.e.,
    ``view[key]``).
    """

    name = None
    """The name of the view, depicting the path taken through the
    configuration in Python-like syntax (e.g., ``foo['bar'][42]``).
    """

    def resolve(self):
        """The core (internal) data retrieval method. Generates (value,
        source) pairs for each source that contains a value for this
        view. May raise ConfigTypeError if a type error occurs while
        traversing a source.
        """
        raise NotImplementedError

    def first(self) -> Any:
        """Return a (value, source) pair for the first object found for
        this view. This amounts to the first element returned by
        `resolve`. If no values are available, a ConfigNotFoundError is
        raised.
        """
        pairs = self.resolve()
        try:
            return iter_first(pairs)
        except ValueError:
            raise ConfigNotFoundError("{0} not found".format(self.name))

    def exists(self) -> bool:
        """Determine whether the view has a setting in any source.
        """
        try:
            self.first()
        except ConfigNotFoundError:
            return False
        return True

    def add(self, value):
        """Set the *default* value for this configuration view. The
        specified value is added as the lowest-priority configuration
        data source.
        """
        raise NotImplementedError

    def set(self, value):
        """*Override* the value for this configuration view. The
        specified value is added as the highest-priority configuration
        data source.
        """
        raise NotImplementedError

    def root(self):
        """The RootView object from which this view is descended.
        """
        raise NotImplementedError

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.name)

    def __iter__(self):
        # Prevent list(config) from using __getitem__ and entering an
        # infinite loop.
        raise TypeError(
            "{!r} object is not " "iterable".format(self.__class__.__name__)
        )

    def __getitem__(self, key: Union[str, int]) -> Any:
        """Get a subview of this view."""
        return Subview(self, key)

    def __setitem__(self, key: int, value: bool) -> None:
        """Create an overlay source to assign a given key under this
        view.
        """
        self.set({key: value})

    def __contains__(self, key: int) -> bool:
        return self[key].exists()

    def set_args(self, namespace):
        """Overlay parsed command-line arguments, generated by a library
        like argparse or optparse, onto this view's value.
        """
        args = {}
        for key, value in namespace.__dict__.items():
            if value is not None:  # Avoid unset options.
                args[key] = value
        self.set(args)

    # Magical conversions. These special methods make it possible to use
    # View objects somewhat transparently in certain circumstances. For
    # example, rather than using ``view.get(bool)``, it's possible to
    # just say ``bool(view)`` or use ``view`` in a conditional.

    def __str__(self) -> str:
        """Get the value for this view as a string.
        """
        return str(self.get())

    def __bool__(self) -> bool:
        """Gets the value for this view as a boolean.
        """
        return bool(self.get())

    # Dictionary emulation methods.

    def keys(self) -> Union[List[Union[str, int]], List[int], List[str]]:
        """Returns a list containing all the keys available as subviews
        of the current views. This enumerates all the keys in *all*
        dictionaries matching the current view, in contrast to
        ``view.get(dict).keys()``, which gets all the keys for the
        *first* dict matching the view. If the object for this view in
        any source is not a dict, then a ConfigTypeError is raised. The
        keys are ordered according to how they appear in each source.
        """
        keys = []

        for dic, _ in self.resolve():
            try:
                cur_keys = dic.keys()
            except AttributeError:
                raise ConfigTypeError(
                    "{0} must be a dict, not {1}".format(self.name, type(dic).__name__)
                )

            for key in cur_keys:
                if key not in keys:
                    keys.append(key)

        return keys

    def items(self) -> Iterator[Union[Tuple[str, Subview], Tuple[int, Subview]]]:
        """Iterates over (key, subview) pairs contained in dictionaries
        from *all* sources at this view. If the object for this view in
        any source is not a dict, then a ConfigTypeError is raised.
        """
        for key in self.keys():
            yield key, self[key]

    def values(self) -> Iterator[Subview]:
        """Iterates over all the subviews contained in dictionaries from
        *all* sources at this view. If the object for this view in any
        source is not a dict, then a ConfigTypeError is raised.
        """
        for key in self.keys():
            yield self[key]

    # List/sequence emulation.

    def all_contents(self) -> Iterator[int]:
        """Iterates over all subviews from collections at this view from
        *all* sources. If the object for this view in any source is not
        iterable, then a ConfigTypeError is raised. This method is
        intended to be used when the view indicates a list; this method
        will concatenate the contents of the list from all sources.
        """
        for collection, _ in self.resolve():
            try:
                it = iter(collection)
            except TypeError:
                raise ConfigTypeError(
                    "{0} must be an iterable, not {1}".format(
                        self.name, type(collection).__name__
                    )
                )
            for value in it:
                yield value

    # Validation and conversion.

    def flatten(
        self,
        redact: bool = False,
        dclass: Union[Type["ConfigDict"], Type[OrderedDict]] = OrderedDict,
    ) -> Union[OrderedDict, "ConfigDict"]:
        """Create a hierarchy of dclass containing the data from
        this view, recursively reifying all views to get their
        represented values.

        If `redact` is set, then sensitive values are replaced with
        the string "REDACTED".
        """
        od = dclass()
        for key, view in self.items():
            if redact and view.redact:
                od[key] = REDACTED_TOMBSTONE
            else:
                try:
                    od[key] = view.flatten(redact=redact, dclass=dclass)
                except ConfigTypeError:
                    od[key] = view.get()
        return od

    def get(self, template: None = None) -> Any:
        """Retrieve the value for this view according to the template.

        The `template` against which the values are checked can be
        anything convertible to a `Template` using `as_template`. This
        means you can pass in a default integer or string value, for
        example, or a type to just check that something matches the type
        you expect.

        May raise a `ConfigValueError` (or its subclass,
        `ConfigTypeError`) or a `ConfigNotFoundError` when the configuration
        doesn't satisfy the template.
        """
        return as_template(template).value(self, template)

    # Old validation methods (deprecated).

    # def as_filename(self):
    #     return self.get(Filename())

    # def as_choice(self, choices):
    #     return self.get(Choice(choices))

    # def as_number(self):
    #     return self.get(Number())

    # def as_str_seq(self):
    #     return self.get(StrSeq())

    # Redaction.

    @property
    def redact(self):
        """Whether the view contains sensitive information and should be
        redacted from output.
        """
        return () in self.get_redactions()

    @redact.setter
    def redact(self, flag):
        self.set_redaction((), flag)

    def set_redaction(self, path, flag):
        """Add or remove a redaction for a key path, which should be an
        iterable of keys.
        """
        raise NotImplementedError()

    def get_redactions(self):
        """Get the set of currently-redacted sub-key-paths at this view.
        """
        raise NotImplementedError()


class RootView(ConfigView):
    """The base of a view hierarchy. This view keeps track of the
    sources that may be accessed by subviews.
    """

    def __init__(self, sources: List[ConfigSource]) -> None:
        """Create a configuration hierarchy for a list of sources. At
        least one source must be provided. The first source in the list
        has the highest priority.
        """
        self.sources = list(sources)
        self.name = ROOT_NAME
        self.redactions = set()

    def add(self, obj: Union[Dict[str, str], ConfigSource]) -> None:
        self.sources.append(ConfigSource.of(obj))

    def set(self, value: Union[Dict[str, str], Dict[int, bool], ConfigSource]) -> None:
        self.sources.insert(0, ConfigSource.of(value))

    def resolve(self) -> Iterator[Any]:
        return ((dict(s), s) for s in self.sources)

    def clear(self) -> None:
        """Remove all sources (and redactions) from this
        configuration.
        """
        del self.sources[:]
        self.redactions.clear()

    # https://mypy.readthedocs.io/en/stable/dynamic_typing.html
    def root(self) -> "RootView":
        return self

    def set_redaction(self, path: int, flag: str) -> None:
        if flag:
            self.redactions.add(path)
        elif path in self.redactions:
            self.redactions.remove(path)

    def get_redactions(self) -> Set[int]:
        return self.redactions


class Subview(ConfigView):
    """A subview accessed via a subscript of a parent view."""

    # NOTE: https://stackoverflow.com/questions/33837918/type-hints-solve-circular-dependency
    def __init__(
        self,
        parent: Union[BaseConfiguration, "Configuration", Subview, RootView],
        key: Union[str, int],
    ) -> None:
        """Make a subview of a parent view for a given subscript key.
        """
        self.parent = parent
        self.key = key

        # Choose a human-readable name for this view.
        if isinstance(self.parent, RootView):
            self.name = ""
        else:
            self.name = self.parent.name
            if not isinstance(self.key, int):
                self.name += "."
        if isinstance(self.key, int):
            self.name += "#{0}".format(self.key)
        elif isinstance(self.key, str):
            if isinstance(self.key, bytes):
                self.name += self.key.decode("utf8")
            else:
                self.name += self.key
        else:
            self.name += repr(self.key)

    def resolve(
        self,
    ) -> Iterator[Union[Tuple[OrderedDict, ConfigSource], Tuple[int, ConfigSource]]]:
        for collection, source in self.parent.resolve():
            try:
                value = collection[self.key]
            except IndexError:
                # List index out of bounds.
                continue
            except KeyError:
                # Dict key does not exist.
                continue
            except TypeError:
                # Not subscriptable.
                raise ConfigTypeError(
                    "{0} must be a collection, not {1}".format(
                        self.parent.name, type(collection).__name__
                    )
                )
            yield value, source

    def set(self, value):
        self.parent.set({self.key: value})

    def add(self, value):
        self.parent.add({self.key: value})

    def root(self) -> RootView:
        return self.parent.root()

    def set_redaction(self, path, flag):
        self.parent.set_redaction((self.key,) + path, flag)

    def get_redactions(self):
        return (
            kp[1:] for kp in self.parent.get_redactions() if kp and kp[0] == self.key
        )


# TODO: This is cli specific right now, let's update this to be more generic
# Config file paths, including platform-specific paths and in-package
# defaults.


def config_dirs(domain: str = "user", override: Optional[str] = None) -> List[str]:
    """Return a platform-specific list of candidates for user
    configuration directories on the system.

    The candidates are in order of priority, from highest to lowest. The
    last element is the "fallback" location to be used when no
    higher-priority config file exists.
    """
    paths = []
    if domain is "user":
        if platform.system() == "Darwin":
            # TODO: Add this back in one day # paths.append(MAC_DIR)
            paths.append(UNIX_DIR_FALLBACK)
            # if UNIX_DIR_VAR in os.environ:
            #     paths.append(os.environ[UNIX_DIR_VAR])

        # elif platform.system() == "Windows":
        #     if WINDOWS_DIR_VAR in os.environ:
        #         paths.append(os.environ[WINDOWS_DIR_VAR])
        #     paths.append(WINDOWS_DIR_FALLBACK)

        else:
            # Assume Unix.
            paths.append(UNIX_DIR_FALLBACK)
            # if UNIX_DIR_VAR in os.environ:
            #     paths.append(os.environ[UNIX_DIR_VAR])

    # TODO: JONES, When you come back, finish making this base config etc into proper broken out objects
    # This is for alternate configurations like the system wide one used in running packs/actions/etc
    if domain is "system":
        paths.append(UNIX_SYSTEM_DIR)

    # mainly for testing etc
    if override:
        # empty list then add only override
        paths = []
        paths.append(override)

    # Expand and deduplicate paths.
    out = []
    for path in paths:
        path = os.path.abspath(os.path.expanduser(path))
        if path not in out:
            out.append(path)
    return out


# YAML loading.


class Loader(yaml.SafeLoader):
    """A customized YAML loader. This loader deviates from the official
    YAML spec in a few convenient ways:

    - All strings as are Unicode objects.
    - All maps are OrderedDicts.
    - Strings can begin with % without quotation.
    """

    # All strings should be Unicode objects, regardless of contents.
    def _construct_unicode(self, node: ScalarNode) -> str:
        return self.construct_scalar(node)

    # Use ordered dictionaries for every YAML map.
    # From https://gist.github.com/844388
    def construct_yaml_map(self, node: MappingNode) -> Iterator[OrderedDict]:
        data = OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node: MappingNode, deep: bool = False) -> OrderedDict:
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(
                None,
                None,
                "expected a mapping node, but found %s" % node.id,
                node.start_mark,
            )

        mapping = OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "found unacceptable key (%s)" % exc,
                    key_node.start_mark,
                )
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping

    # Allow bare strings to begin with %. Directives are still detected.
    def check_plain(self) -> bool:
        plain = super().check_plain()
        return plain or self.peek() == "%"


Loader.add_constructor("tag:yaml.org,2002:str", Loader._construct_unicode)
Loader.add_constructor("tag:yaml.org,2002:map", Loader.construct_yaml_map)
Loader.add_constructor("tag:yaml.org,2002:omap", Loader.construct_yaml_map)


def load_yaml(filename):
    """Read a YAML document from a file. If the file cannot be read or
    parsed, a ConfigReadError is raised.
    """
    try:
        with open(filename, "r") as f:
            return yaml.load(f, Loader=Loader)
    except (IOError, yaml.error.YAMLError) as exc:
        raise ConfigReadError(filename, exc)


# TODO: We need a standalone function to save data to yaml
# def save_yaml(filename, data):
#     """
#     Save contents of an OrderedDict structure to a yaml file
#     :param filename: name of the yaml file to save to
#     :type filename: str
#     :param data: configuration data to to save
#     :type filename: str
#     :type data: OrderedDict

#     :returns: Nothing
#     """

#     ordered = type(data).__name__ == "OrderedDict"
#     dict_type = "dict"
#     if ordered:
#         dict_type = "OrderedDict"
#     LOGGER.info("Saving '{}' to '{}'".format(dict_type, filename))
#     if ordered:
#         sdata = _ordered_dump(
#             data,
#             Dumper=yaml.SafeDumper,
#             indent=4,
#             width=768,
#             allow_unicode=True,
#             default_flow_style=False,
#         )
#     else:
#         sdata = yaml.dump(
#             data,
#             Dumper=yaml.SafeDumper,
#             indent=4,
#             width=768,
#             allow_unicode=True,
#             default_flow_style=False,
#         )
#     sdata = _format_yaml_dump(sdata)
#     with open(filename, "w") as outfile:
#        outfile.write(sdata)

# YAML dumping.


class Dumper(yaml.SafeDumper):
    """A PyYAML Dumper that represents OrderedDicts as ordinary mappings
    (in order, of course).
    """

    # From http://pyyaml.org/attachment/ticket/161/use_ordered_dict.py
    def represent_mapping(
        self, tag: str, mapping: OrderedDict, flow_style: None = None
    ) -> MappingNode:
        value = []
        node = yaml.MappingNode(tag, value, flow_style=flow_style)
        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node
        best_style = False
        if hasattr(mapping, "items"):
            mapping = mapping.items()
        for item_key, item_value in mapping:
            node_key = self.represent_data(item_key)
            node_value = self.represent_data(item_value)
            if not (isinstance(node_key, yaml.ScalarNode) and not node_key.style):
                best_style = False
            if not (isinstance(node_value, yaml.ScalarNode) and not node_value.style):
                best_style = False
            value.append((node_key, node_value))
        if flow_style is None:
            if self.default_flow_style is not None:
                node.flow_style = self.default_flow_style
            else:
                node.flow_style = best_style
        return node

    def represent_list(self, data):
        """If a list has less than 4 items, represent it in inline style
        (i.e. comma separated, within square brackets).
        """
        node = super().represent_list(data)
        length = len(data)
        if self.default_flow_style is None and length < 4:
            node.flow_style = True
        elif self.default_flow_style is None:
            node.flow_style = False
        return node

    def represent_bool(self, data):
        """Represent bool as 'yes' or 'no' instead of 'true' or 'false'.
        """
        if data:
            value = "yes"
        else:
            value = "no"
        return self.represent_scalar("tag:yaml.org,2002:bool", value)

    def represent_none(self, data):
        """Represent a None value with nothing instead of 'none'.
        """
        return self.represent_scalar("tag:yaml.org,2002:null", "")


Dumper.add_representer(OrderedDict, Dumper.represent_dict)
Dumper.add_representer(bool, Dumper.represent_bool)
Dumper.add_representer(type(None), Dumper.represent_none)
Dumper.add_representer(list, Dumper.represent_list)


def restore_yaml_comments(data: str, default_data: str) -> str:
    """Scan default_data for comments (we include empty lines in our
    definition of comments) and place them before the same keys in data.
    Only works with comments that are on one or more own lines, i.e.
    not next to a yaml mapping.
    """
    comment_map = dict()
    default_lines = iter(default_data.splitlines())
    for line in default_lines:
        if not line:
            comment = "\n"
        elif line.startswith("#"):
            comment = "{0}\n".format(line)
        else:
            continue
        while True:
            line = next(default_lines)
            if line and not line.startswith("#"):
                break
            comment += "{0}\n".format(line)
        key = line.split(":")[0].strip()
        comment_map[key] = comment
    out_lines = iter(data.splitlines())
    out_data = ""
    for line in out_lines:
        key = line.split(":")[0].strip()
        if key in comment_map:
            out_data += comment_map[key]
        out_data += "{0}\n".format(line)
    return out_data


# Base interface. ( NOTE, this is basically the cli config at this moment, need to modify it to work with other types of configs )

############################################################################################################
class BaseConfiguration(RootView):
    def __init__(
        self, appname: str, modname: Optional[str] = None, read: bool = True
    ) -> None:
        """Create a configuration object by reading the
        automatically-discovered config files for the application for a
        given name. If `modname` is specified, it should be the import
        name of a module whose package will be searched for a default
        config file. (Otherwise, no defaults are used.) Pass `False` for
        `read` to disable automatic reading of all discovered
        configuration files. Use this when creating a configuration
        object at module load time and then call the `read` method
        later.
        """
        super().__init__([])
        self.appname = appname
        self.modname = modname

        self.config_filename = "smart.yaml"
        self.default_filename = "smart_default.yaml"
        self.domain = "user"  # Domain tells the config_dirs command which code path to follow to find the correct location to find configuration files

        self._env_var = "{0}DIR".format(self.appname.upper())

        if read:
            self.read()

    # TODO: rename this config_path instead of config_path. Then implement where that values lies in templated/subclasses
    def config_path(self) -> str:
        """Points to the location of the user configuration.

        The file may not exist.
        """
        return os.path.join(self.config_dir(), self.config_filename)

    # TODO: rename this _add_source instead of _add_source. Then implement where that values lies in templated/subclasses
    def _add_source(self) -> None:
        """Add the configuration options from the YAML file in the
        user's configuration directory (given by `config_dir`) if it
        exists.
        """
        filename = self.config_path()
        if os.path.isfile(filename):
            self.add(ConfigSource(load_yaml(filename) or {}, filename))

    # TODO: Maybe change this to not implemented or create a BaseClass that everything can adhere to. Else, simply template the other classes and make sure the code to pull this value is different and appropiate ( eg. packs, actions, etc )
    def _add_default_source(self) -> None:
        """Add the package's default configuration settings. This looks
        for a YAML file located inside the package for the module
        `modname` if it was given.
        """
        if self.modname:
            filename = pkg_resources.resource_filename(self.modname, DEFAULT_FILENAME)
            if os.path.isfile(filename):
                self.add(ConfigSource(load_yaml(filename), filename, True))

    # TODO: rename arguments? instead of user, switch it to source? Defaults keep the same, maybe add one more value to allow us to override? (do we need that) ?
    def read(self, source: bool = True, defaults: bool = True) -> None:
        """Find and read the files for this configuration and set them
        as the sources for this configuration. To disable either
        discovered source configuration files or the in-package defaults,
        set `source` or `defaults` to `False`.
        """
        if source:
            self._add_source()
        if defaults:
            self._add_default_source()

    def check_path_for_correct_subdir(self, path):
        p = Path(path).resolve()
        # In [9]: p.parts
        # Out[9]: ('/', 'Users', 'malcolm', '.config')
        if (
            self.appname in p.parts[-1]
        ):  # if ultron8 is the name of the top level config folder
            return True
        else:
            return False

    # TODO: Need to make this interchangeable so that we can use this class to load yaml files for packs, actions, etc etc
    def config_dir(self) -> str:
        """Get the path to the user configuration directory. The
        directory is guaranteed to exist as a postcondition (one may be
        created if none exist).

        If the application's ``...DIR`` environment variable is set, it
        is used as the configuration directory. Otherwise,
        platform-specific standard configuration locations are searched
        for a ``config.yaml`` file. If no configuration file is found, a
        fallback path is used.
        """
        # If environment variable is set, use it.
        if self._env_var in os.environ:
            logger.debug(" [config_dir] inside environment variable section")
            # appdir = os.path.join(os.environ[self._env_var], self.appname)
            appdir = os.environ[self._env_var]
            logger.debug(" [config_dir] initial value appdir = {}".format(appdir))
            appdir = os.path.abspath(
                os.path.expanduser(appdir)
            )  # NOTE: This should be something like ~/.config/ultron8
            logger.debug(
                " [config_dir] after expanduser value appdir = {}".format(appdir)
            )

            # # now check to see if ultron8 is in the path name, if not, append it
            # if not self.check_path_for_correct_subdir(appdir):
            #     appdir = os.path.join(appdir, self.appname)

            if os.path.isfile(appdir):
                raise ConfigError("{0} must be a directory".format(self._env_var))

        else:
            # Search platform-specific locations. If no config file is
            # found, fall back to the final directory in the list.
            for confdir in config_dirs(domain=self.domain):
                appdir = os.path.join(confdir, self.appname)
                if os.path.isfile(os.path.join(appdir, self.config_filename)):
                    break

        # Ensure that the directory exists.
        if not os.path.isdir(appdir):
            os.makedirs(appdir)
        return appdir

    def set_file(self, filename: str) -> None:
        """Parses the file as YAML and inserts it into the configuration
        sources with highest priority.
        """
        filename = os.path.abspath(filename)
        self.set(ConfigSource(load_yaml(filename), filename))

    def dump(self, full: bool = True, redact: bool = False) -> str:
        """Dump the Configuration object to a YAML file.

        The order of the keys is determined from the default
        configuration file. All keys not in the default configuration
        will be appended to the end of the file.

        :param filename:  The file to dump the configuration to, or None
                          if the YAML string should be returned instead
        :type filename:   unicode
        :param full:      Dump settings that don't differ from the defaults
                          as well
        :param redact:    Remove sensitive information (views with the `redact`
                          flag set) from the output
        """
        if full:
            out_dict = self.flatten(redact=redact)
        else:
            # Exclude defaults when flattening.
            sources = [s for s in self.sources if not s.default]
            temp_root = RootView(sources)
            temp_root.redactions = self.redactions
            out_dict = temp_root.flatten(redact=redact)

        yaml_out = yaml.dump(
            out_dict, Dumper=Dumper, default_flow_style=None, indent=4, width=1000
        )

        # Restore comments to the YAML text.
        default_source = None
        for source in self.sources:
            if source.default:
                default_source = source
                break
        if default_source and default_source.filename:
            with open(default_source.filename, "r") as fp:
                default_data = fp.read()
            yaml_out = restore_yaml_comments(yaml_out, default_data)

        return yaml_out


REQUIRED = object()
"""A sentinel indicating that there is no default value and an exception
should be raised when the value is missing.
"""


class Template(object):
    """A value template for configuration fields.

    The template works like a type and instructs Confuse about how to
    interpret a deserialized YAML value. This includes type conversions,
    providing a default value, and validating for errors. For example, a
    filepath type might expand tildes and check that the file exists.
    """

    def __init__(self, default: object = REQUIRED) -> None:
        """Create a template with a given default value.

        If `default` is the sentinel `REQUIRED` (as it is by default),
        then an error will be raised when a value is missing. Otherwise,
        missing values will instead return `default`.
        """
        self.default = default

    def __call__(self, view):
        """Invoking a template on a view gets the view's value according
        to the template.
        """
        return self.value(view, self)

    def value(
        self, view: Union[BaseConfiguration, Subview, RootView], template: None = None
    ) -> Any:
        """Get the value for a `ConfigView`.

        May raise a `ConfigNotFoundError` if the value is missing (and the
        template requires it) or a `ConfigValueError` for invalid values.
        """
        if view.exists():
            value, _ = view.first()
            return self.convert(value, view)
        elif self.default is REQUIRED:
            # Missing required value. This is an error.
            raise ConfigNotFoundError("{0} not found".format(view.name))
        else:
            # Missing value, but not required.
            return self.default

    def convert(
        self, value: Any, view: Union[RootView, Subview, BaseConfiguration]
    ) -> Any:
        """Convert the YAML-deserialized value to a value of the desired
        type.

        Subclasses should override this to provide useful conversions.
        May raise a `ConfigValueError` when the configuration is wrong.
        """
        # Default implementation does no conversion.
        return value

    def fail(self, message, view, type_error=False):
        """Raise an exception indicating that a value cannot be
        accepted.

        `type_error` indicates whether the error is due to a type
        mismatch rather than a malformed value. In this case, a more
        specific exception is raised.
        """
        exc_class = ConfigTypeError if type_error else ConfigValueError
        raise exc_class("{0}: {1}".format(view.name, message))

    def __repr__(self):
        return "{0}({1})".format(
            type(self).__name__, "" if self.default is REQUIRED else repr(self.default),
        )


class Integer(Template):
    """An integer configuration value template.
    """

    def convert(self, value, view):
        """Check that the value is an integer. Floats are rounded.
        """
        if isinstance(value, int):
            return value
        elif isinstance(value, float):
            return int(value)
        else:
            self.fail("must be a number", view, True)


class Number(Template):
    """A numeric type: either an integer or a floating-point number.
    """

    def convert(self, value, view):
        """Check that the value is an int or a float.
        """
        if isinstance(value, (int, float)):
            return value
        else:
            self.fail(
                "must be numeric, not {0}".format(type(value).__name__), view, True
            )


class MappingTemplate(Template):
    """A template that uses a dictionary to specify other types for the
    values for a set of keys and produce a validated `AttrDict`.
    """

    def __init__(self, mapping):
        """Create a template according to a dict (mapping). The
        mapping's values should themselves either be Types or
        convertible to Types.
        """
        subtemplates = {}
        for key, typ in mapping.items():
            subtemplates[key] = as_template(typ)
        self.subtemplates = subtemplates

    def value(self, view, template=None):
        """Get a dict with the same keys as the template and values
        validated according to the value types.
        """
        out = AttrDict()
        for key, typ in self.subtemplates.items():
            out[key] = typ.value(view[key], self)
        return out

    def __repr__(self):
        return "MappingTemplate({0})".format(repr(self.subtemplates))


class String(Template):
    """A string configuration value template.
    """

    def __init__(self, default=REQUIRED, pattern=None):
        """Create a template with the added optional `pattern` argument,
        a regular expression string that the value should match.
        """
        super().__init__(default)
        self.pattern = pattern
        if pattern:
            self.regex = re.compile(pattern)

    def __repr__(self):
        args = []

        if self.default is not REQUIRED:
            args.append(repr(self.default))

        if self.pattern is not None:
            args.append("pattern=" + repr(self.pattern))

        return "String({0})".format(", ".join(args))

    def convert(self, value, view):
        """Check that the value is a string and matches the pattern.
        """
        if isinstance(value, str):
            if self.pattern and not self.regex.match(value):
                self.fail("must match the pattern {0}".format(self.pattern), view)
            return value
        else:
            self.fail("must be a string", view, True)


class Choice(Template):
    """A template that permits values from a sequence of choices.
    """

    def __init__(self, choices):
        """Create a template that validates any of the values from the
        iterable `choices`.

        If `choices` is a map, then the corresponding value is emitted.
        Otherwise, the value itself is emitted.
        """
        self.choices = choices

    def convert(self, value, view):
        """Ensure that the value is among the choices (and remap if the
        choices are a mapping).
        """
        if value not in self.choices:
            self.fail(
                "must be one of {0}, not {1}".format(
                    repr(list(self.choices)), repr(value)
                ),
                view,
            )

        if isinstance(self.choices, abc.Mapping):
            return self.choices[value]
        else:
            return value

    def __repr__(self):
        return "Choice({0!r})".format(self.choices)


class OneOf(Template):
    """A template that permits values complying to one of the given templates.
    """

    def __init__(self, allowed, default=REQUIRED):
        super().__init__(default)
        self.allowed = list(allowed)

    def __repr__(self):
        args = []

        if self.allowed is not None:
            args.append("allowed=" + repr(self.allowed))

        if self.default is not REQUIRED:
            args.append(repr(self.default))

        return "OneOf({0})".format(", ".join(args))

    def value(self, view, template):
        self.template = template
        return super().value(view, template)

    def convert(self, value, view):
        """Ensure that the value follows at least one template.
        """
        is_mapping = isinstance(self.template, MappingTemplate)

        for candidate in self.allowed:
            try:
                if is_mapping:
                    if isinstance(candidate, Filename) and candidate.relative_to:
                        next_template = candidate.template_with_relatives(
                            view, self.template
                        )

                        next_template.subtemplates[view.key] = as_template(candidate)
                    else:
                        next_template = MappingTemplate({view.key: candidate})

                    return view.parent.get(next_template)[view.key]
                else:
                    return view.get(candidate)
            except ConfigTemplateError:
                raise
            except ConfigError:
                pass
            except ValueError as exc:
                raise ConfigTemplateError(exc)

        self.fail(
            "must be one of {0}, not {1}".format(repr(self.allowed), repr(value)), view
        )


class StrSeq(Template):
    """A template for values that are lists of strings.

    Validates both actual YAML string lists and single strings. Strings
    can optionally be split on whitespace.
    """

    def __init__(self, split=True):
        """Create a new template.

        `split` indicates whether, when the underlying value is a single
        string, it should be split on whitespace. Otherwise, the
        resulting value is a list containing a single string.
        """
        super().__init__()
        self.split = split

    def convert(self, value, view):
        if isinstance(value, bytes):
            value = value.decode("utf8", "ignore")

        if isinstance(value, str):
            if self.split:
                return value.split()
            else:
                return [value]

        try:
            value = list(value)
        except TypeError:
            self.fail("must be a whitespace-separated string or a list", view, True)

        def convert(x):
            if isinstance(x, str):
                return x
            elif isinstance(x, bytes):
                return x.decode("utf8", "ignore")
            else:
                self.fail("must be a list of strings", view, True)

        return list(map(convert, value))


class Filename(Template):
    """A template that validates strings as filenames.

    Filenames are returned as absolute, tilde-free paths.

    Relative paths are relative to the template's `cwd` argument
    when it is specified, then the configuration directory (see
    the `config_dir` method) if they come from a file. Otherwise,
    they are relative to the current working directory. This helps
    attain the expected behavior when using command-line options.
    """

    def __init__(self, default=REQUIRED, cwd=None, relative_to=None, in_app_dir=False):
        """`relative_to` is the name of a sibling value that is
        being validated at the same time.

        `in_app_dir` indicates whether the path should be resolved
        inside the application's config directory (even when the setting
        does not come from a file).
        """
        super().__init__(default)
        self.cwd = cwd
        self.relative_to = relative_to
        self.in_app_dir = in_app_dir

    def __repr__(self):
        args = []

        if self.default is not REQUIRED:
            args.append(repr(self.default))

        if self.cwd is not None:
            args.append("cwd=" + repr(self.cwd))

        if self.relative_to is not None:
            args.append("relative_to=" + repr(self.relative_to))

        if self.in_app_dir:
            args.append("in_app_dir=True")

        return "Filename({0})".format(", ".join(args))

    def resolve_relative_to(self, view, template):
        if not isinstance(template, (abc.Mapping, MappingTemplate)):
            # disallow config.get(Filename(relative_to='foo'))
            raise ConfigTemplateError(
                "relative_to may only be used when getting multiple values."
            )

        elif self.relative_to == view.key:
            raise ConfigTemplateError("{0} is relative to itself".format(view.name))

        elif self.relative_to not in list(view.parent.keys()):
            # self.relative_to is not in the config
            self.fail(
                ('needs sibling value "{0}" to expand relative path').format(
                    self.relative_to
                ),
                view,
            )

        old_template = {}
        old_template.update(template.subtemplates)

        # save time by skipping MappingTemplate's init loop
        next_template = MappingTemplate({})
        next_relative = self.relative_to

        # gather all the needed templates and nothing else
        while next_relative is not None:
            try:
                # pop to avoid infinite loop because of recursive
                # relative paths
                rel_to_template = old_template.pop(next_relative)
            except KeyError:
                if next_relative in template.subtemplates:
                    # we encountered this config key previously
                    raise ConfigTemplateError(
                        ("{0} and {1} are recursively relative").format(
                            view.name, self.relative_to
                        )
                    )
                else:
                    raise ConfigTemplateError(
                        (
                            "missing template for {0}, needed to expand {1}'s"
                            + "relative path"
                        ).format(self.relative_to, view.name)
                    )

            next_template.subtemplates[next_relative] = rel_to_template
            next_relative = rel_to_template.relative_to

        return view.parent.get(next_template)[self.relative_to]

    def value(self, view, template=None):
        path, source = view.first()
        if not isinstance(path, str):
            self.fail(
                "must be a filename, not {0}".format(type(path).__name__), view, True
            )
        path = os.path.expanduser(str(path))

        if not os.path.isabs(path):
            if self.cwd is not None:
                # relative to the template's argument
                path = os.path.join(self.cwd, path)

            elif self.relative_to is not None:
                path = os.path.join(self.resolve_relative_to(view, template), path,)

            elif source.filename or self.in_app_dir:
                # From defaults: relative to the app's directory.
                path = os.path.join(view.root().config_dir(), path)

        return os.path.abspath(path)


class TypeTemplate(Template):
    """A simple template that checks that a value is an instance of a
    desired Python type.
    """

    def __init__(self, typ, default=REQUIRED):
        """Create a template that checks that the value is an instance
        of `typ`.
        """
        super().__init__(default)
        self.typ = typ

    def convert(self, value, view):
        if not isinstance(value, self.typ):
            self.fail(
                "must be a {0}, not {1}".format(
                    self.typ.__name__, type(value).__name__,
                ),
                view,
                True,
            )
        return value


class AttrDict(dict):
    """A `dict` subclass that can be accessed via attributes (dot
    notation) for convenience.
    """

    def __getattr__(self, key):
        if key in self:
            return self[key]
        else:
            raise AttributeError(key)


def as_template(value: None) -> Template:
    """Convert a simple "shorthand" Python value to a `Template`.
    """
    if isinstance(value, Template):
        # If it's already a Template, pass it through.
        return value
    elif isinstance(value, abc.Mapping):
        # Dictionaries work as templates.
        return MappingTemplate(value)
    elif value is int:
        return Integer()
    elif isinstance(value, int):
        return Integer(value)
    elif isinstance(value, type) and issubclass(value, str):
        return String()
    elif isinstance(value, str):
        return String(value)
    elif isinstance(value, set):
        # convert to list to avoid hash related problems
        return Choice(list(value))
    elif isinstance(value, list):
        return OneOf(value)
    elif value is float:
        return Number()
    elif value is None:
        return Template()
    elif value is dict:
        return TypeTemplate(abc.Mapping)
    elif value is list:
        return TypeTemplate(abc.Sequence)
    elif isinstance(value, type):
        return TypeTemplate(value)
    else:
        raise ValueError("cannot convert to template: {0!r}".format(value))
