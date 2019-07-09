#!/usr/bin/env python
""" This script reverse engineers the protocols defined in pilight.
    It converts them to voloptuous schemes to allow protocol validation
    before sending data to the pilight daemon.
    'git' python package has to be installed.
    TODO: use regex for numbers
"""
# SOURCE: https://github.com/DavidLP/pilight/blob/a319404034e761892a89c7205b6f1aff6ad8e205/scripts/create_validators.py
import glob
import re

import voluptuous as vol

# import git

# git.Repo.clone_from(url=r'https://github.com/pilight/pilight',
#                 to_path='pilight')


def parse_option(option_string):
    if "OPTION_NO_VALUE" in option_string:
        option = re.findall(r"\"(.*?)\"", option_string)[0]
        # The options without values seem to still need a value
        # when used with pilight-daemon, but this are not mandatory
        # options
        # E.G.: option 'on' is 'on': 1
        return {vol.Optional(option): vol.Coerce(int)}
    elif "OPTION_HAS_VALUE" in option_string:
        options = re.findall(r"\"(.*?)\"", option_string)
        option = options[0]
        regex = None
        if len(options) > 1:  # Option has specified value by regex
            regex = options[1]
        if "JSON_NUMBER" in option_string:
            return {vol.Required(option): vol.Coerce(int)}
        elif "JSON_STRING" in option_string:
            return {vol.Required(option): vol.Coerce(str)}
        else:
            raise
    elif "OPTION_OPT_VALUE" in option_string:
        options = re.findall(r"\"(.*?)\"", option_string)
        option = options[0]
        regex = None
        if len(options) > 1:  # Option has specified value by regex
            regex = options[1]
        if "JSON_NUMBER" in option_string:
            return {vol.Required(option): vol.Coerce(int)}
        elif "JSON_STRING" in option_string:
            return {vol.Required(option): vol.Coerce(str)}
        else:
            raise
    else:
        print(option_string)
        raise

    raise


def parse_protocol(file):
    protocol = {}
    with open(file, "r") as in_file:
        for line in in_file:
            # Omit commented code
            if "//" in line:
                continue
            # Omit GUI specific protocol settings
            if "GUI_SETTING" in line:
                continue
            # Get protocol id (= name string)
            if "protocol_set_id" in line:
                p_id = line.partition('"')[-1].rpartition('"')[0]
            # Get protocol options (key/value pairs)
            if "options_add" in line:
                protocol.update(parse_option(line))

    return {p_id: protocol}


# def parse_yaml_config(file):


def get_protocols(path="pilight/**/433*/*.c"):
    for filename in glob.iglob(path, recursive=True):
        yield filename


# dump(ruamel.yaml)
# ['AliasEvent',
#  'AliasToken',
#  'AnchorToken',
#  'BaseConstructor',
#  'BaseDumper',
#  'BaseLoader',
#  'BaseRepresenter',
#  'BlockEndToken',
#  'BlockEntryToken',
#  'BlockMappingStartToken',
#  'BlockSequenceStartToken',
#  'BytesIO',
#  'CBaseDumper',
#  'CBaseLoader',
#  'CDumper',
#  'CEmitter',
#  'CLoader',
#  'CParser',
#  'CSafeDumper',
#  'CSafeLoader',
#  'CollectionEndEvent',
#  'CollectionNode',
#  'CollectionStartEvent',
#  'CommentCheck',
#  'CommentToken',
#  'Constructor',
#  'DirectiveToken',
#  'DocumentEndEvent',
#  'DocumentEndToken',
#  'DocumentStartEvent',
#  'DocumentStartToken',
#  'Dumper',
#  'Event',
#  'FlowEntryToken',
#  'FlowMappingEndToken',
#  'FlowMappingStartToken',
#  'FlowSequenceEndToken',
#  'FlowSequenceStartToken',
#  'KeyToken',
#  'Loader',
#  'MappingEndEvent',
#  'MappingNode',
#  'MappingStartEvent',
#  'Node',
#  'NodeEvent',
#  'PY3',
#  'Representer',
#  'Resolver',
#  'RoundTripConstructor',
#  'RoundTripDumper',
#  'RoundTripLoader',
#  'RoundTripRepresenter',
#  'SHOWLINES',
#  'SafeConstructor',
#  'SafeDumper',
#  'SafeLoader',
#  'SafeRepresenter',
#  'ScalarEvent',
#  'ScalarNode',
#  'ScalarToken',
#  'SequenceEndEvent',
#  'SequenceNode',
#  'SequenceStartEvent',
#  'StreamEndEvent',
#  'StreamEndToken',
#  'StreamStartEvent',
#  'StreamStartToken',
#  'StringIO',
#  'TagToken',
#  'Token',
#  'UnsafeLoader',
#  'UnsafeLoaderWarning',
#  'ValueToken',
#  'VersionedResolver',
#  'YAML',
#  'YAMLContextManager',
#  'YAMLError',
#  'YAMLObject',
#  'YAMLObjectMetaclass',
#  '__builtins__',
#  '__cached__',
#  '__doc__',
#  '__file__',
#  '__loader__',
#  '__name__',
#  '__package__',
#  '__path__',
#  '__spec__',
#  '__version__',
#  '__with_libyaml__',
#  '_package_data',
#  'absolute_import',
#  'add_constructor',
#  'add_implicit_resolver',
#  'add_multi_constructor',
#  'add_multi_representer',
#  'add_path_resolver',
#  'add_representer',
#  'comments',
#  'compat',
#  'compose',
#  'compose_all',
#  'composer',
#  'constructor',
#  'cyaml',
#  'division',
#  'dump',
#  'dump_all',
#  'dumper',
#  'emit',
#  'emitter',
#  'enc',
#  'enforce',
#  'error',
#  'events',
#  'glob',
#  'import_module',
#  'load',
#  'load_all',
#  'loader',
#  'main',
#  'nodes',
#  'nprint',
#  'os',
#  'parse',
#  'parser',
#  'print_function',
#  'reader',
#  'representer',
#  'resolver',
#  'round_trip_dump',
#  'round_trip_load',
#  'round_trip_load_all',
#  'ruamel',
#  'safe_dump',
#  'safe_dump_all',
#  'safe_load',
#  'safe_load_all',
#  'scalarfloat',
#  'scalarint',
#  'scalarstring',
#  'scan',
#  'scanner',
#  'serialize',
#  'serialize_all',
#  'serializer',
#  'string_types',
#  'sys',
#  'timestamp',
#  'tokens',
#  'unicode_literals',
#  'util',
#  'version_info',
#  'warnings',
#  'with_metaclass',
#  'yaml_object']

if __name__ == "__main__":

    protocols = None
    for protocol in get_protocols():
        if not protocols:
            # , extra=vol.ALLOW_EXTRA)
            protocols = vol.Schema(
                parse_protocol(protocol),
                # Allows additional protcols but
                # also additional protcol keys
                # HOWTO fix?
                extra=vol.ALLOW_EXTRA,
            )
        else:
            protocols.extend(parse_protocol(protocol))
