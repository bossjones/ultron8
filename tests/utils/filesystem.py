import logging

logger = logging.getLogger(__name__)


def helper_write_yaml_to_disk(data, path, additional_data=None):
    with open(path, "wt") as f:
        f.write(data)
