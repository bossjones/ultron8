"""Test shell utils"""
# pylint: disable=protected-access
import logging

import pytest
from six.moves import zip

from ultron8.utils.shell import quote_unix

logger = logging.getLogger(__name__)


@pytest.mark.utilsonly
@pytest.mark.unittest
class TestShellUtilsTestCase:
    def test_quote_unix(self):
        arguments = ["foo", "foo bar", "foo1 bar1", '"foo"', '"foo" "bar"', "'foo bar'"]
        expected_values = [
            """
            foo
            """,
            """
            'foo bar'
            """,
            """
            'foo1 bar1'
            """,
            """
            '"foo"'
            """,
            """
            '"foo" "bar"'
            """,
            """
            ''"'"'foo bar'"'"''
            """,
        ]

        for argument, expected_value in zip(arguments, expected_values):
            actual_value = quote_unix(value=argument)
            expected_value = expected_value.lstrip()
            assert actual_value == expected_value.strip()
