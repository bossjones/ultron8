import json

from ultron8.logging_init import getLogger

logger = getLogger(__name__)


def write_file(file_path, contents, mode="w"):
    with open(file_path, mode, encoding="utf-8") as file_handle:
        file_handle.write(contents)


def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file_handle:
        content = file_handle.read().replace("\n", "")
    return json.loads(content)


def write_json_file(file_path, data):
    write_file(file_path, json.dumps(data))
