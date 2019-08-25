from collections import OrderedDict, defaultdict
import json
from typing import Dict


def snake_to_title(target):
    return "".join(segment.title() for segment in target.split("_"))


def sort_dict(value):
    """Sort a dictionary."""
    return OrderedDict((key, value[key]) for key in sorted(value))


def generate_list_of_ordereddict(list_of_unordered_dict):
    data = defaultdict(list)

    # data = sort_dict({key: sort_dict(value) for key, value in data.items()})
    # return BASE.format(json.dumps(data, indent=4))
