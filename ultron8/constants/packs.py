# A list of allowed characters for the pack name
PACK_REF_WHITELIST_REGEX = r"^[a-z0-9_]+$"

# Check for a valid semver string
PACK_VERSION_REGEX = r"^(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-[\da-z\-]+(?:\.[\da-z\-]+)*)?(?:\+[\da-z\-]+(?:\.[\da-z\-]+)*)?$"  # noqa

# Special characters which can't be used in pack names
PACK_RESERVED_CHARACTERS = ["."]

# Version sperator when version is supplied in pack name
# Example: libcloud@1.0.1
PACK_VERSION_SEPARATOR = "="

# Name used for system pack
SYSTEM_PACK_NAME = "core"

# Name used for pack management pack
PACKS_PACK_NAME = "packs"

# Name used for linux pack
LINUX_PACK_NAME = "linux"

# Name of the default pack
DEFAULT_PACK_NAME = "default"

# Name of the chatops pack
CHATOPS_PACK_NAME = "chatops"

# A list of system pack names
SYSTEM_PACK_NAMES = [
    CHATOPS_PACK_NAME,
    SYSTEM_PACK_NAME,
    PACKS_PACK_NAME,
    LINUX_PACK_NAME,
]

# A list of pack names which can't be used by user-supplied packs
USER_PACK_NAME_BLACKLIST = [SYSTEM_PACK_NAME, PACKS_PACK_NAME]

# Python requirements which are common to all the packs and are installed into the Python pack
# sandbox (virtualenv)
BASE_PACK_REQUIREMENTS = ["six>=1.9.0,<2.0"]

# Python requirements which are common to all the packs and need to be installed
# for Python 3 pack virtual environments to work
BASE_PACK_PYTHON3_REQUIREMENTS = ["pyyaml>=3.12,<4.0"]

# Name of the pack manifest file
MANIFEST_FILE_NAME = "pack.yaml"

# File name for the config schema file
CONFIG_SCHEMA_FILE_NAME = "config.schema.yaml"
