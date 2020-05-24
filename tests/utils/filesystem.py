import logging
from typing import Optional

logger = logging.getLogger(__name__)


def helper_write_yaml_to_disk(
    data: str, path: str, additional_data: None = None
) -> None:
    with open(path, "wt") as f:
        f.write(data)
