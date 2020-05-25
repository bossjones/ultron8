"""Test Utils."""
# pylint: disable=protected-access
import logging

import pytest

import ultron8
from ultron8.utils import dict_merge
from ultron8.utils import maybe_decode
from ultron8.utils import maybe_encode
from ultron8.utils import next_or_none

logger = logging.getLogger(__name__)


@pytest.mark.utilsonly
@pytest.mark.unittest
class DictMergeTestCase:
    def test_merges_dicts(self):
        a = {
            "a": 1,
            "b": {"b1": 2, "b2": 3,},
        }
        b = {
            "a": 1,
            "b": {"b1": 4,},
        }

        assert dict_merge(a, b)["a"] == 1
        assert dict_merge(a, b)["b"]["b2"] == 3
        assert dict_merge(a, b)["b"]["b1"] == 4

    def test_inserts_new_keys(self):
        """Will it insert new keys by default?"""
        a = {
            "a": 1,
            "b": {"b1": 2, "b2": 3,},
        }
        b = {
            "a": 1,
            "b": {"b1": 4, "b3": 5},
            "c": 6,
        }

        assert dict_merge(a, b)["a"] == 1
        assert dict_merge(a, b)["b"]["b2"] == 3
        assert dict_merge(a, b)["b"]["b1"] == 4
        assert dict_merge(a, b)["b"]["b3"] == 5
        assert dict_merge(a, b)["c"] == 6

    def test_does_not_insert_new_keys(self):
        """Will it avoid inserting new keys when required?"""
        a = {
            "a": 1,
            "b": {"b1": 2, "b2": 3,},
        }
        b = {
            "a": 1,
            "b": {"b1": 4, "b3": 5,},
            "c": 6,
        }

        assert dict_merge(a, b, add_keys=False)["a"] == 1
        assert dict_merge(a, b, add_keys=False)["b"]["b2"] == 3
        assert dict_merge(a, b, add_keys=False)["b"]["b1"] == 4
        try:
            assert dict_merge(a, b, add_keys=False)["b"]["b3"] == 5
        except KeyError:
            pass
        else:
            raise Exception("New keys added when they should not be")

        try:
            assert dict_merge(a, b, add_keys=False)["b"]["b3"] == 6
        except KeyError:
            pass
        else:
            raise Exception("New keys added when they should not be")


@pytest.mark.utilsonly
@pytest.mark.unittest
class TestStringsUtils:
    def test_maybe_decode(self):
        a_maybe_string = b"file:///etc/fstab"
        assert maybe_decode(a_maybe_string) == "file:///etc/fstab"

    def test_maybe_encode(self):
        a_maybe_string = "file:///etc/fstab"
        assert maybe_encode(a_maybe_string) == b"file:///etc/fstab"

    def test_next_or_none(self):
        a = [1, 2, 3, 4]
        assert next_or_none(r for r in a if a != 0) == 1
