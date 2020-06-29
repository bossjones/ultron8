# st2common
import yaml

__all__ = ["ALLOWED_EXTS", "PARSER_FUNCS"]

ALLOWED_EXTS = [".yaml", ".yml"]
PARSER_FUNCS = {".yml": yaml.safe_load, ".yaml": yaml.safe_load}
