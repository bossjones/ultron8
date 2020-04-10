import os
from pathlib import Path

# from dotenv import load_dotenv
# from .paths import env_dir
from ultron8.api.middleware.logging.log import logger


# def load_env(target):
#     target_file = target + ".env"
#     target_path = env_dir(target_file)
#     if Path(target_path).is_file():
#         logger.debug(f"loading {target} environment")
#         load_dotenv(dotenv_path=target_path)
#     else:
#         logger.warning(f"failed to load {target} environment file")


def setenv(key, val):
    os.environ[key] = val


def getenv(key, default=None, optional=False):
    val = os.getenv(key, default)
    if not val and not optional:
        raise Exception(f"Value {key} cannot be null")
    return val


def getenv_bool(var_name, default=False, optional=False):
    result = default
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


# from piviti
def get_bool_env(var):
    value = os.getenv(var)
    if not value:
        return False
    value = value.lower()
    if value == "False":
        return False
    if value == "0":
        return False
    else:
        return bool(value)


# from piviti
def get_env_by_type(type_, var):
    """Gets an environment variable.

    Args:
        type_ (type): The type of the variable.
        var (str): The name of the environment variable.

    Returns:
        The contents of the environment variable, or None if it doesn't exist.
    """
    if var is None:
        return None
    if type_ == bool:
        return get_bool_env(var)
    value = os.getenv(var)
    if value:
        return type_(os.getenv(var))
    return None
