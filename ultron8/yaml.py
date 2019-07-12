# -*- coding: utf-8 -*-
"""Yaml Utility functions"""
# pylint: disable=line-too-long
# pylint: disable=W1202
# flake8: noqa
import collections
import functools
import keyword
import logging
import os
import shutil
import sys
from collections import OrderedDict

from ultron8.consts import CONF_FILE
from ultron8.consts import DEBUG_MODE_FLAG
from ultron8.consts import YAML_FILE

LOGGER = logging.getLogger(__name__)

try:
    if DEBUG_MODE_FLAG:
        # Catch all fatal errors
        from IPython.core.debugger import Tracer  # noqa
        from IPython.core import ultratb

        sys.excepthook = ultratb.FormattedTB(
            mode="Verbose", color_scheme="Linux", call_pdb=True, ostream=sys.__stdout__
        )

        from ultron8 import debugger
        from ultron8.debugger import (
            debug_dump,
            dump_all,
            dump_color,
            dump_dict,
            dump_dir,
            dump_magic,
            dump_vars,
            get_pprint,
        )
except ImportError as exc:
    output = "WARNING: Ipython not imported, fatal error handler not initialized. If you don't want to automatically step into pdb on exception, then ignore this error message. Module= {}".format(
        __name__
    )
    LOGGER.warning(output)

INTEGER_TYPES = (int,)
STRING_TYPES = (str,)
TEXT_TYPE = str

try:
    import ruamel.yaml as yaml
    from ruamel.yaml.error import YAMLError  # pragma: no cover

    EDITING_ENABLED = True

except Exception as e:
    EDITING_ENABLED = False
    LOGGER.critical("ultron8.yaml: ruamel.yaml is not installed")
    exit(1)

yaml_version = "1.2"
indent_spaces = 4
block_seq_indent = 0


def editing_is_enabled():
    return EDITING_ENABLED == True


def convert_linenumber(s, occ=1):
    if occ == 1:
        s2 = s[s.find("line: ") + 6 :]
    elif occ == 2:
        p = s.find("line: ") + 6
        s2 = s[s.find("line: ", p) + 6 :]
    else:
        return "*" + s
    lineold = s2[: s2.find(")")]
    linenew = str(int((int(lineold) + 1) / 2))
    lo = "line " + lineold
    ln = "line " + linenew
    lo2 = "(line: " + lineold + ")"
    ln2 = "(line: " + linenew + ")"
    s = s.replace(lo, ln)
    s = s.replace(lo2, ln2)
    return s


def yaml_load(filename, ordered=False, ignore_notfound=False):
    """
    Load contents of a configuration file into an dict/OrderedDict structure. The configuration file has to be a valid yaml file

    :param filename: name of the yaml file to load
    :type filename: str
    :param ordered: load to an OrderedDict? Default=False
    :type ordered: bool

    :return: configuration data loaded from the file (or None if an error occured)
    :rtype: Dict | OrderedDict | None
    """

    dict_type = "dict"
    if ordered:
        dict_type = "OrderedDict"
    LOGGER.info("Loading '{}' to '{}'".format(filename, dict_type))
    y = None

    try:
        with open(filename, "r") as stream:
            sdata = stream.read()
        sdata = sdata.replace("\n", "\n\n")
        if ordered:
            y = _ordered_load(sdata, yaml.SafeLoader)
        else:
            y = yaml.load(sdata, yaml.SafeLoader)
    except Exception as e:
        estr = str(e)
        if "found character '\\t'" in estr:
            estr = estr[estr.find("line") :]
            estr = (
                "TABs are not allowed in YAML files, use spaces for indentation instead!\nError in "
                + estr
            )
        if ("while scanning a simple key" in estr) and (
            "could not found expected ':'" in estr
        ):
            estr = estr[estr.find("column") : estr.find("could not")]
            estr = (
                "The colon (:) following a key has to be followed by a space. The space is missing!\nError in "
                + estr
            )
        if "(line: " in estr:
            line = convert_linenumber(estr)
            line = convert_linenumber(line, 2)
            #            estr += '\nNOTE: To find correct line numbers: add 1 to line and divide by 2 -> '+line
            estr = line
            estr += "\nNOTE: Look for the error at the expected <block end>, near the second specified line number"
        if "[Errno 2]" in estr:
            if not ignore_notfound:
                LOGGER.warning("YAML-file not found: {}".format(filename))
        else:
            LOGGER.error("YAML-file load error in {}:  \n{}".format(filename, estr))

    return y


def yaml_load_fromstring(string, ordered=False):
    """
    Load contents of a string into an dict/OrderedDict structure. The string has to be valid yaml

    :param string: name of the yaml file to load
    :type string: str
    :param ordered: load to an OrderedDict? Default=False
    :type ordered: bool

    :return: configuration data loaded from the file (or None if an error occured)
    :rtype: Dict | OrderedDict | None
    """

    dict_type = "dict"
    if ordered:
        dict_type = "OrderedDict"
    LOGGER.info("Loading '{}' to '{}'".format(string, dict_type))
    y = None

    estr = ""
    try:
        sdata = string
        #        sdata = sdata.replace('\n', '\n\n')
        if ordered:
            y = _ordered_load(sdata, yaml.SafeLoader)
        else:
            y = yaml.load(sdata, yaml.SafeLoader)
    except Exception as e:
        estr = str(e)
        if "found character '\\t'" in estr:
            estr = estr[estr.find("line") :]
            estr = (
                "TABs are not allowed in YAML files, use spaces for indentation instead!\nError in "
                + estr
            )
        if ("while scanning a simple key" in estr) and (
            "could not found expected ':'" in estr
        ):
            estr = estr[estr.find("column") : estr.find("could not")]
            estr = (
                "The colon (:) following a key has to be followed by a space. The space is missing!\nError in "
                + estr
            )

    return y, estr


def yaml_save(filename, data):
    """
    Save contents of an OrderedDict structure to a yaml file
    :param filename: name of the yaml file to save to
    :type filename: str
    :param data: configuration data to to save
    :type filename: str
    :type data: OrderedDict

    :returns: Nothing
    """

    ordered = type(data).__name__ == "OrderedDict"
    dict_type = "dict"
    if ordered:
        dict_type = "OrderedDict"
    LOGGER.info("Saving '{}' to '{}'".format(dict_type, filename))
    if ordered:
        sdata = _ordered_dump(
            data,
            Dumper=yaml.SafeDumper,
            indent=4,
            width=768,
            allow_unicode=True,
            default_flow_style=False,
        )
    else:
        sdata = yaml.dump(
            data,
            Dumper=yaml.SafeDumper,
            indent=4,
            width=768,
            allow_unicode=True,
            default_flow_style=False,
        )
    sdata = _format_yaml_dump(sdata)
    with open(filename, "w") as outfile:
        outfile.write(sdata)


# ==================================================================================


def _format_yaml_load(data):
    """
    Reinsert '\n's that have been removed fom comments to make file more readable
    :param data: string to format

    :return: formatted string
    """

    #    ptr = 0
    #    cptr = data[ptr:].find('comment: ')

    data = data.replace("\n", "\n\n")
    return data


def _ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    """
    Ordered yaml loader
    Use this instead ot yaml.loader/yaml.saveloader to get an Ordereddict
    :param stream: stream to read from
    :param Loader: yaml-loader to use
    :object_pairs_hook: ...

    :return: OrderedDict structure
    """

    # usage example: ordered_load(stream, yaml.SafeLoader)
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
    )
    return yaml.load(stream, OrderedLoader)


def _format_yaml_dump(data):
    """
    Format yaml-dump to make file more readable
    (yaml structure must be dumped to a stream before using this function)
    | Currently does the following:
    | - Add an empty line before a new item
    :param data: string to format

    :return: formatted string
    """

    data = data.replace("\n\n", "\n")
    ldata = data.split("\n")
    rdata = []
    for index, line in enumerate(ldata):
        if line[-1:] == ":":
            # no empty line before list attributes
            if ldata[index + 1].strip()[0] != "-":
                rdata.append("")
            rdata.append(line)
        else:
            rdata.append(line)
    fdata = "\n".join(rdata)
    return fdata


def _ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    """
    Ordered yaml dumper
    Use this instead ot yaml.Dumper/yaml.SaveDumper to get an Ordereddict
    :param stream: stream to write to
    :param Dumper: yaml-dumper to use
    :**kwds: Additional keywords

    :return: OrderedDict structure
    """

    # usage example: ordered_dump(data, Dumper=yaml.SafeDumper)
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, list(data.items())
        )

    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


# ==================================================================================
#   Routines to handle editing of yaml files
#


def yaml_load_roundtrip(filename):
    """
    Load contents of a yaml file into an dict structure for editing (using Roundtrip Loader)
    :param filename: name of the yaml file to load
    :return: data structure loaded from file
    """

    if not EDITING_ENABLED:
        return None

    y = None
    try:
        with open(filename + YAML_FILE, "r") as stream:
            sdata = stream.read()
        sdata = sdata.replace("\n", "\n\n")
        y = yaml.load(sdata, yaml.RoundTripLoader)
    except Exception as e:
        LOGGER.error("yaml_load_roundtrip: YAML-file load error: '%s'" % (e))
        y = {}
    return y


def get_emptynode():
    """
   Return an empty node
   """
    return yaml.comments.CommentedMap([])


def get_commentedseq(l):
    """
   Convert a list to a commented sequence
   """
    return yaml.comments.CommentedSeq(l)


def yaml_dump_roundtrip(data):
    """
    Dump yaml to a string using the RoundtripDumper and correct linespacing in output file
    :param data: data structure to save
    """

    sdata = yaml.dump(
        data,
        Dumper=yaml.RoundTripDumper,
        version=yaml_version,
        indent=indent_spaces,
        block_seq_indent=block_seq_indent,
        width=12288,
        allow_unicode=True,
    )
    sdata = _format_yaml_dump2(sdata)
    return sdata


def yaml_save_roundtrip(filename, data, create_backup=False):
    """
    Dump yaml using the RoundtripDumper and correct linespacing in output file
    :param filename: name of the yaml file to save to
    :param data: data structure to save
    """

    if not EDITING_ENABLED:
        return
    sdata = yaml.dump(
        data,
        Dumper=yaml.RoundTripDumper,
        version=yaml_version,
        indent=indent_spaces,
        block_seq_indent=block_seq_indent,
        width=12288,
        allow_unicode=True,
    )
    sdata = _format_yaml_dump2(sdata)

    if create_backup:
        if os.path.isfile(filename + YAML_FILE):
            shutil.copy2(filename + YAML_FILE, filename + ".bak")

    with open(filename + YAML_FILE, "w") as outfile:
        outfile.write(sdata)


def _strip_empty_lines(data):
    ldata = data.split("\n")

    rdata = []
    for index, line in enumerate(ldata):
        if len(line.strip()) == 0:
            line = line.strip()
        rdata.append(line)

    fdata = "\n".join(rdata)
    if fdata[0] == "\n":
        fdata = fdata[1:]
    return fdata


def _format_yaml_dump2(sdata):
    """
    Format yaml-dump to make file more readable, used by yaml_save_roundtrip()
    (yaml structure must be dumped to a stream before using this function)
    | Currently does the following:
    | - Insert empty line after section w/o a value
    | - Insert empty line before section (key w/o a value)
    | - Adjust indentation of list entries
    | - Remove double line spacing introduced by ruamel.yaml
    | - Multiline strings: Remove '4' inserted by ruamel.yaml after '|'
    | - Remove empty line after section w/o a value, if the following line is a child-line
    :param data: string to format

    :return: formatted string
    """

    # Strip lines containing only spaces and strip empty lines inserted by ruamel.yaml
    sdata = _strip_empty_lines(sdata)
    sdata = sdata.replace("\n\n\n", "\n")
    sdata = sdata.replace("\n\n", "\n")
    #    sdata = sdata.replace(': |4\n', ': |\n')    # Multiline strings: remove '4' inserted by ruyaml

    ldata = sdata.split("\n")
    rdata = []
    for index, line in enumerate(ldata):
        # Remove empty line after section w/o a value, if the following line is a child-line
        if len(line.strip()) == 0:
            try:
                nextline = ldata[index + 1]
            except Exception as e:
                nextline = ""
            indentprevline = len(ldata[index - 1]) - len(ldata[index - 1].lstrip(" "))
            indentnextline = len(nextline) - len(nextline.lstrip(" "))
            if indentnextline != indentprevline + indent_spaces:
                rdata.append(line)
        # Insert empty line after section w/o a value
        elif len(line.lstrip()) > 0 and line.lstrip()[0] == "#":
            if line.lstrip()[-1:] == ":":
                rdata.append("")
            # only insert empty line, if last line was not a comment
            elif len(ldata[index - 1].strip()) > 0 and ldata[index - 1][0] != "#":
                # Only insert empty line, if next line is not commented out
                if (
                    len(ldata[index + 1].strip()) > 0
                    and ldata[index + 1][-1:] == ":"
                    and ldata[index + 1][0] != "#"
                ):
                    rdata.append("")
            rdata.append(line)

        # Insert empty line before section (key w/o a value)
        elif line[-1:] == ":":
            # only, if last line is not empty and last line is not a comment
            if len(ldata[index - 1].lstrip()) > 0 and not (
                len(ldata[index - 1].lstrip()) > 0
                and ldata[index - 1].lstrip()[0] == "#"
            ):
                # no empty line before list attributes
                if ldata[index + 1].strip() != "":
                    if ldata[index + 1].strip()[0] != "-":
                        rdata.append("")
                else:
                    rdata.append("")
                rdata.append(line)
            else:
                rdata.append(line)
        else:
            rdata.append(line)

    sdata = "\n".join(rdata)

    sdata = sdata.replace("\n---\n\n", "\n---\n")
    if sdata[0] == "\n":
        sdata = sdata[1:]
    return sdata


# ==================================================================================
#   support functions for class yamlfile
#

# Set a given data in a dictionary with position provided as a list
def setInDict(dataDict, path, value):
    mapList = path.split(".")
    try:
        for k in mapList[:-1]:
            dataDict = dataDict[k]
        dataDict[mapList[-1]] = value
    except Exception as e:
        return False
    return True


# Get parent to a path
def get_parent(path):
    pathlist = path.split(".")
    parent = ".".join(pathlist[0 : len(pathlist) - 1])
    return parent


# Get key without parent
def get_key(path):
    pathlist = path.split(".")
    key = pathlist[len(pathlist) - 1]
    return key


# ==================================================================================
#   function for changing a single item-attribute in a yaml file
#


def writeBackToFile(filename, itempath, itemattr, value):
    """
    write the value of an item's attribute back to the yaml-file
    :param filename: name of the yaml-file (without the .yaml extension!)
    :param itempath: path of the item to modify
    :param itemattr: name of the item's attribute to modify
    :param value: new value for the attribute
    :return: formatted string
    """

    itemyamlfile = yamlfile(filename)
    if os.path.isfile(filename + YAML_FILE):
        itemyamlfile.load()
    itemyamlfile.setleafvalue(itempath, itemattr, value)
    itemyamlfile.save()


# ==================================================================================
#   class yamlfile (for editing multiple entries at a time)
#


class yamlfile:
    data = None
    filename = ""

    def __init__(self, filename, filename_write="", create_bak=False):
        """
        initialize class for handling a yaml-file (read/write)
        | It initializes an empty data-structure, which can be filled by the load() method
        | This class is to be used for editing of yaml-files, not for loading SmartHomeNG structures
        :param filename: name of the yaml-file (without the .yaml extension!)
        :param filename_write: name of the file to write the resluts to (if different from filename)
        :param create_bak: True, if a backup-file of the original file shall be created

        :return: formatted string
        """
        self.filename = filename
        if filename_write == "":
            self.filename_write = filename
        else:
            self.filename_write = filename_write
        self.filename_bak = self.filename_write + ".bak" + YAML_FILE
        self._create_bak = create_bak
        self.data = yaml.comments.CommentedMap([])

    def load(self):
        """
        load the contents of the yaml-file to the data-structure
        """
        self.data = yaml_load_roundtrip(self.filename)

    def save(self):
        """
        save the contents of the data-structure to the yaml-file
        """
        if self._create_bak and os.path.isfile(self.filename_write + YAML_FILE):
            os.rename(self.filename_write + YAML_FILE, self.filename_bak)
        yaml_save_roundtrip(self.filename_write, self.data)

    def getnode(self, path):
        """
        get the contents of a node (branch or leaf)

        :param path: path of the node to return

        :return: content of the node
        """
        returned, ret_nodetype = self._getFromDict(path)
        return returned

    def getvalue(self, path):
        """
        get the value of a leaf-node

        :param path: path of the node to return

        :return: value of the leaf (or None, if the node is no leaf-node)
        """
        returned, ret_nodetype = self._getFromDict(path)
        if ret_nodetype == "leaf":
            return returned
        else:
            return None

    def getnodetype(self, path):
        """
        get the type of a node

        :param path: path of the node to return

        :return: node type ('branch', 'leaf' or 'none')
        """
        returned, ret_nodetype = self._getFromDict(path)
        return ret_nodetype

    def getvaluetype(self, path):
        """
        get the valuetype of a node

        :param path: path of the node to return

        :return: node valuetype
        """
        returned, ret_nodetype = self._getFromDict(path)
        result = str(type(returned))
        if result[0:8] == "<class '":
            result = result[8:-2]
        if result == "ruamel.yaml.comments.CommentedSeq":
            result = "list"
        return result

    # Add/set a leaf to an empty node, the branch node must exist
    def setvalue(self, path, value):
        """
        set the value of a leaf, specified by leaf-path

        :param path: path of the leaf-node to modify
        :param value: new value of the leaf-node
        """
        if value == None:
            try:
                self.getnode(get_parent(path)).pop(get_key(path), None)
            except AttributeError:
                pass
            if self.getnode(get_parent(path)) == yaml.comments.CommentedMap():
                node = self.getnode(get_parent(get_parent(path)))
                root = node == None
                if root:
                    self.data[get_key(get_parent(path))] = None
                else:
                    node[get_key(get_parent(path))] = None
            return
        else:
            return self._add_node_and_leaf(path, value)

    # Add/set a leaf with value, the branch is created if it does not exist
    def setleafvalue(self, branch, leaf, value):
        """
        set the value of a leaf, specified by branch-path and attribute name

        :param branch: path of the branch-node which contains th attribute
        :param attr: name of the attribute to modify
        :param value: new value of the attribute
        """
        try:
            self._ensurebranch(branch)
        except Exception as e:
            LOGGER.error("setleafvalue: Exception '{}'".format(str(e)))
        else:
            if value != None:
                self.setvalue(branch + "." + leaf, value)

    # ----------------------------------------------------------

    # Add an empty branch
    def _ensurebranch(self, path):
        if self.getnodetype(path) == "leaf":
            raise KeyError(
                "Node-ERROR: Unable to set branch '"
                + path
                + "', it exists already as a leaf"
            )
        elif self.getnodetype(path) == "branch":
            pass
        else:
            if not self._addnode(path):
                raise KeyError(
                    "Node-ERROR: Unable to set branch '" + path + "' in item structure"
                )

    # Add an empty branch
    def _addbranch(self, path):
        if self.getnodetype(path) == "leaf":
            raise KeyError(
                "Node-ERROR: Unable to set branch '"
                + path
                + "', it exists already as a leaf"
            )
        elif self.getnodetype(path) == "branch":
            raise KeyError(
                "Node-ERROR: Unable to set branch '"
                + path
                + "', it exists already as a branch"
            )
        else:
            if not self._addnode(path):
                raise KeyError(
                    "Node-ERROR: Unable to set branch '" + path + "' in item structure"
                )

    # Add an empty node (internal for recursion)
    def _addnode(self, path):
        if self.getnodetype(path) != "none":
            return False
        result = self._add_node_and_leaf(path, None)
        if not result:
            pathlist = path.split(".")
            parent = ".".join(pathlist[0 : len(pathlist) - 1])
            if self._addnode(parent):
                result = self._add_node_and_leaf(path, None)
        return result

    # Add a leaf to an empty node
    def _add_node_and_leaf(self, path, value):
        if not setInDict(self.data, path, value):
            parent = get_parent(path)
            attr = path[len(parent) + 1 :]
            cm = yaml.comments.CommentedMap([(attr, value)])
            if not setInDict(self.data, parent, cm):
                return False
        return True

    # Get a given data from a dictionary with position provided as a list
    def _getFromDict(self, path):
        dataDict = self.data
        nodetype = "-"
        mapList = path.split(".")
        try:
            for k in mapList:
                dataDict = dataDict[k]
        except Exception as e:
            nodetype = "none"
            dataDict = None
        else:
            if isinstance(dataDict, yaml.comments.CommentedMap):
                nodetype = "branch"
            else:
                nodetype = "leaf"
        return dataDict, nodetype


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# End of shyaml
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Begin of config
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>


# import lib.shyaml as shyaml
# LOGGER = logging.getLogger(__name__)

valid_item_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
valid_attr_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_@*"
digits = "0123456789"
reserved = ["set", "get"]

REMOVE_ATTR = "attr"
REMOVE_PATH = "path"


def parse_basename(basename, configtype=""):
    """
    Load and parse a single configuration and merge it to the configuration tree
    The configuration is only specified by the basename.
    At the moment it looks for a .yaml file or a .conf file
    .yaml files take preference

    :param basename: Name of the configuration
    :param configtype: Optional string with config type (only used for log output)
    :type basename: str
    :type configtype: str

    :return: The resulting merged OrderedDict tree
    :rtype: OrderedDict

    """
    config = parse(basename + YAML_FILE)
    if config == {}:
        config = parse(basename + CONF_FILE)
    if config == {}:
        if not (configtype == "logics"):
            LOGGER.critical(
                "No file '{}.*' found with {} configuration".format(
                    basename, configtype
                )
            )
    return config


def parse_itemsdir(itemsdir, item_conf, addfilenames=False):
    """
    Load and parse item configurations and merge it to the configuration tree
    The configuration is only specified by the name of the directory.
    At the moment it looks for .yaml files and a .conf files
    Both filetypes are read, even if they have the same basename

    :param itemsdir: Name of folder containing the configuration files
    :param item_conf: Optional OrderedDict tree, into which the configuration should be merged
    :type itemsdir: str
    :type item_conf: OrderedDict
    :return: The resulting merged OrderedDict tree
    :rtype: OrderedDict
    """
    for item_file in sorted(os.listdir(itemsdir)):
        if item_file.endswith(CONF_FILE) or item_file.endswith(YAML_FILE):
            if item_file == "logic" + YAML_FILE and itemsdir.find("lib/env/") > -1:
                LOGGER.info(
                    "config.parse_itemsdir: skipping logic definition file = {}".format(
                        itemsdir + item_file
                    )
                )
            else:
                try:
                    item_conf = parse(itemsdir + item_file, item_conf, addfilenames)
                except Exception as e:
                    LOGGER.exception("Problem reading {0}: {1}".format(item_file, e))
                    continue
    return item_conf


def parse(filename, config=None, addfilenames=False):
    """
    Load and parse a configuration file and merge it to the configuration tree
    Depending on the extension of the filename, the apropriate parser is called

    :param filename: Name of the configuration file
    :param config: Optional OrderedDict tree, into which the configuration should be merged
    :type filename: str
    :type config: OrderedDict
    :return: The resulting merged OrderedDict tree
    :rtype: OrderedDict
    """
    if filename.endswith(YAML_FILE) and os.path.isfile(filename):
        return parse_yaml(filename, config, addfilenames)
    elif filename.endswith(CONF_FILE) and os.path.isfile(filename):
        return parse_conf(filename, config)
    return {}


# --------------------------------------------------------------------------------------


def remove_keys(ydata, func, remove=[REMOVE_ATTR], level=0, msg=None, key_prefix=""):
    """
    Removes given keys from a dict or OrderedDict structure
    :param ydata: configuration (sub)tree to work on
    :param func: the function to call to check for removal (Example: lambda k: k.startswith('comment'))
    :param level: optional subtree level (used for recursion)
    :type ydata: OrderedDict
    :type func: function
    :type level: int

    """
    try:
        level_keys = list(ydata.keys())
        for key in level_keys:
            key_str = str(key)
            key_dict = type(ydata[key]).__name__ in ["dict", "OrderedDict"]
            if not key_dict:
                key_remove = REMOVE_ATTR in remove and func(key_str)
            else:
                key_remove = REMOVE_PATH in remove and func(key_str)
            if key_remove:
                if msg:
                    LOGGER.warning(msg.format(key_prefix + key_str))
                ydata.pop(key)
            elif key_dict:
                remove_keys(
                    ydata[key], func, remove, level + 1, msg, key_prefix + key_str + "."
                )
    except Exception as e:
        LOGGER.error(
            "Problem removing key from '{}', probably invalid YAML file: {}".format(
                str(ydata), e
            )
        )


def remove_comments(ydata):
    """
    Removes comments from a dict or OrderedDict structure
    :param ydata: configuration (sub)tree to work on
    :type ydata: OrderedDict

    """
    remove_keys(ydata, lambda k: k.startswith("comment"), [REMOVE_ATTR])


def remove_digits(ydata):
    """
    Removes keys starting with digits from a dict or OrderedDict structure
    :param ydata: configuration (sub)tree to work on
    :type ydata: OrderedDict
    """
    remove_keys(
        ydata,
        lambda k: k[0] in digits,
        [REMOVE_ATTR, REMOVE_PATH],
        msg="Problem parsing '{}': item starts with digits",
    )


def remove_reserved(ydata):
    """
    Removes keys that are reserved keywords from a dict or OrderedDict structure
    :param ydata: configuration (sub)tree to work on
    :type ydata: OrderedDict
    """
    remove_keys(
        ydata,
        lambda k: k in reserved,
        [REMOVE_PATH],
        msg="Problem parsing '{}': item using reserved word set/get",
    )


def remove_keyword(ydata):
    """
    Removes keys that are reserved Python keywords from a dict or OrderedDict structure
    :param ydata: configuration (sub)tree to work on
    :type ydata: OrderedDict
    """
    remove_keys(
        ydata,
        lambda k: keyword.iskeyword(k),
        [REMOVE_PATH],
        msg="Problem parsing '{}': item using reserved Python keyword",
    )


def remove_invalid(ydata):
    """
    Removes invalid chars in item from a dict or OrderedDict structure
    :param ydata: configuration (sub)tree to work on
    :type ydata: OrderedDict
    """
    valid_chars = valid_item_chars + valid_attr_chars
    remove_keys(
        ydata,
        lambda k: True
        if True in [True for i in range(len(k)) if k[i] not in valid_chars]
        else False,
        [REMOVE_ATTR, REMOVE_PATH],
        msg="Problem parsing '{}' invalid character. Valid characters are: "
        + str(valid_chars),
    )


def merge(source, destination):
    """
    Merges an OrderedDict Tree into another one

    :param source: source tree to merge into another one
    :param destination: destination tree to merge into
    :type source: OrderedDict
    :type destination: OrderedDict
    :return: Merged configuration tree
    :rtype: OrderedDict
    :Example: Run me with nosetests --with-doctest file.py
    .. code-block:: python
        >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
        >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
        >>> merge(b, a) == { 'first' : { 'all_rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
        True

    """
    try:
        for key, value in list(source.items()):
            if isinstance(value, collections.OrderedDict):
                # get node or create one
                node = destination.setdefault(key, collections.OrderedDict())
                merge(value, node)
            else:
                if type(value).__name__ == "list":
                    destination[key] = value
                else:
                    # convert to string and remove newlines from multiline attributes
                    destination[key] = str(value).replace("\n", "")
    except Exception as e:
        LOGGER.error("Problem merging subtrees, probably invalid YAML file")

    return destination


def parse_yaml(filename, config=None, addfilenames=False):
    """
    Load and parse a yaml configuration file and merge it to the configuration tree
    :param filename: Name of the configuration file
    :param config: Optional OrderedDict tree, into which the configuration should be merged
    :type filename: str
    :type config: bool

    :return: The resulting merged OrderedDict tree
    :rtype: OrderedDict

    The config file should stick to the following setup:
    .. code-block:: yaml
       firstlevel:
           attribute1: xyz
           attribute2: foo
           attribute3: bar

           secondlevel:
               attribute1: abc
               attribute2: bar
               attribute3: foo

               thirdlevel:
                   attribute1: def
                   attribute2: barfoo
                   attribute3: foobar

           anothersecondlevel:
               attribute1: and so on
    where firstlevel, secondlevel, thirdlevel and anothersecondlevel are defined as items and attribute are their respective attribute - value pairs
    Valid characters for the items are a-z and A-Z plus any digit and underscore as second or further characters.
    Valid characters for the attributes are the same as for an item plus @ and *
    """
    LOGGER.debug("parse_yaml: Parsing file {}".format(os.path.basename(filename)))
    if config is None:
        config = collections.OrderedDict()

    items = yaml_load(filename, ordered=True)
    if items is not None:
        remove_comments(items)
        remove_digits(items)
        remove_reserved(items)
        remove_keyword(items)
        remove_invalid(items)

        if addfilenames:
            LOGGER.debug(
                "parse_yaml: Add filename = {} to items".format(
                    os.path.basename(filename)
                )
            )
            _add_filenames_to_config(items, os.path.basename(filename))

        config = merge(items, config)
    return config


def _add_filenames_to_config(items, filename, level=0):
    """
    Adds the name of the config file to the config items

    This routine is used to add the source filename to:
    - be able to display the file an item is defined in (backend page items)
    - to enable editing and storing back of item definitions

    This function calls itself recurselively

    """
    for attr, value in list(items.items()):
        if isinstance(value, dict):
            child_path = dict(value)
            if filename != "":
                value["_filename"] = filename
            _add_filenames_to_config(child_path, filename, level + 1)
    return


# --------------------------------------------------------------------------------------


def strip_quotes(string):
    """
    Strip single-quotes or double-quotes from string beggining and end

    :param string: String to strip the quotes from
    :type string: str

    :return: Stripped string
    :rtype: str

    """
    string = string.strip()
    if len(string) > 0:
        if string[0] in ['"', "'"]:  # check if string starts with ' or "
            if string[0] == string[-1]:  # and end with it
                if string.count(string[0]) == 2:  # if they are the only one
                    string = string[1:-1]  # remove them
    return string


def parse_conf(filename, config=None):
    """
    Load and parse a configuration file which is in the old .conf format of smarthome.py
    and merge it to the configuration tree
    :param filename: Name of the configuration file
    :param config: Optional OrderedDict tree, into which the configuration should be merged
    :type filename: str
    :type config: bool

    :return: The resulting merged OrderedDict tree
    :rtype: OrderedDict
    The config file should stick to the following setup:
    .. code-block:: ini
       [firstlevel]
           attribute1 = xyz
           attribute2 = foo
           attribute3 = bar

           [[secondlevel]]
               attribute1 = abc
               attribute2 = bar
               attribute3 = foo

               [[[thirdlevel]]]
                   attribute1 = def
                   attribute2 = barfoo
                   attribute3 = foobar

           [[anothersecondlevel]]
               attribute1 = and so on
    where firstlevel, secondlevel, thirdlevel and anothersecondlevel are defined as items and attribute are their respective attribute - value pairs
    Valid characters for the items are a-z and A-Z plus any digit and underscore as second or further characters.
    Valid characters for the attributes are the same as for an item plus @ and *
    """

    valid_set = set(valid_attr_chars)
    if config is None:
        config = collections.OrderedDict()
    item = config
    with open(filename, "r", encoding="UTF-8") as f:
        linenu = 0
        parent = collections.OrderedDict()
        lines = iter(f.readlines())
        for raw in lines:
            linenu += 1
            line = raw.lstrip("\\ufeff")  # remove BOM
            while line.rstrip().endswith("\\"):
                linenu += 1
                line = line.rstrip().rstrip("\\") + next(lines, "").lstrip()
            line = line.partition("#")[0].strip()
            if line is "":
                continue
            if line[0] == "[":  # item
                brackets = 0
                level = 0
                closing = False
                for index in range(len(line)):
                    if line[index] == "[" and not closing:
                        brackets += 1
                        level += 1
                    elif line[index] == "]":
                        closing = True
                        brackets -= 1
                    else:
                        closing = True
                        if line[index] not in valid_item_chars + "'":
                            LOGGER.error(
                                "Problem parsing '{}' invalid character in line {}: {}. Valid characters are: {}".format(
                                    filename, linenu, line, valid_item_chars
                                )
                            )
                            return config
                if brackets != 0:
                    LOGGER.error(
                        "Problem parsing '{}' unbalanced brackets in line {}: {}".format(
                            filename, linenu, line
                        )
                    )
                    return config
                name = line.strip("[]")
                name = strip_quotes(name)

                if len(name) == 0:
                    LOGGER.error(
                        "Problem parsing '{}' tried to use an empty item name in line {}: {}".format(
                            filename, linenu, line
                        )
                    )
                    return config
                elif name[0] in digits:
                    LOGGER.error(
                        "Problem parsing '{}': item starts with digit '{}' in line {}: {}".format(
                            filename, name[0], linenu, line
                        )
                    )
                    return config
                elif name in reserved:
                    LOGGER.error(
                        "Problem parsing '{}': item using reserved word set/get in line {}: {}".format(
                            filename, linenu, line
                        )
                    )
                    return config
                elif keyword.iskeyword(name):
                    LOGGER.error(
                        "Problem parsing '{}': item using reserved Python keyword {} in line {}: {}".format(
                            filename, name, linenu, line
                        )
                    )
                    return config

                if level == 1:
                    if name not in config:
                        config[name] = collections.OrderedDict()
                    item = config[name]
                    parents = collections.OrderedDict()
                    parents[level] = item
                else:
                    if level - 1 not in parents:
                        LOGGER.error(
                            "Problem parsing '{}' no parent item defined for item in line {}: {}".format(
                                filename, linenu, line
                            )
                        )
                        return config
                    parent = parents[level - 1]
                    if name not in parent:
                        parent[name] = collections.OrderedDict()
                    item = parent[name]
                    parents[level] = item

            else:  # attribute
                attr, __, value = line.partition("=")
                if not value:
                    continue
                attr = attr.strip()
                if not set(attr).issubset(valid_set):
                    LOGGER.error(
                        "Problem parsing '{}' invalid character in line {}: {}. Valid characters are: {}".format(
                            filename, linenu, attr, valid_attr_chars
                        )
                    )
                    continue

                if len(attr) > 0:
                    if attr[0] in digits:
                        LOGGER.error(
                            "Problem parsing '{}' attrib starts with a digit '{}' in line {}: {}.".format(
                                filename, attr[0], linenu, attr
                            )
                        )
                        continue
                if "|" in value:
                    item[attr] = [strip_quotes(x) for x in value.split("|")]
                else:
                    item[attr] = strip_quotes(value)
        return config


# smoke-tests
if __name__ == "__main__":
    import logging

    # conf_basename = "try"
    # doc = yaml_load_fromstring(fake_yaml, ordered=True)
