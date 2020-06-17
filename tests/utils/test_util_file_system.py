import os
import os.path

import pytest

from ultron8.utils.file_system import get_file_list

CURRENT_DIR = os.path.dirname(__file__)
EXAMPLES_DIR = os.path.join(CURRENT_DIR, "../../../examples/packs/chatops_tutorial")


@pytest.mark.utilsonly
@pytest.mark.unittest
class FileSystemUtilsTestCase:
    def test_get_file_list(self):
        # Standard exclude pattern
        directory = os.path.join(EXAMPLES_DIR, "actions")
        expected = [
            "fail_on_odd.yaml",
            "fail_on_odd_silent.yaml",
            "pizza.py",
            "pizza.yaml",
            "repeat.yaml",
            "workflows/fail_on_odd.yaml",
            "workflows/fail_on_odd_silent.yaml",
        ]
        result = get_file_list(directory=directory, exclude_patterns=["*.pyc"])
        assert expected == result

        # Custom exclude pattern
        expected = ["pizza.py"]
        result = get_file_list(
            directory=directory, exclude_patterns=["*.pyc", "*.yaml"]
        )
        assert expected == result
