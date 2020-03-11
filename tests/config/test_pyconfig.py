"""Test Global Pyconfig setter/getters."""
# pylint: disable=protected-access
import logging
import pytest
import pyconfig

from ultron8.config import do_set_flag
from ultron8.config import do_get_flag
from ultron8.config import do_set_multi_flag

logger = logging.getLogger(__name__)


@pytest.mark.configonly
@pytest.mark.unittest
class TestPyConfig:
    def test_do_set_flag(self) -> None:
        do_set_flag("test.fake.foo", "bar")
        assert pyconfig.get("test.fake.foo") == "bar"

    def test_do_set_get_flag(self) -> None:
        do_set_flag("test.fake.foo", "bar1")
        assert pyconfig.get("test.fake.foo") == do_get_flag("test.fake.foo")

    def test_set_multi_get_multi(self):
        multi_data = []
        multi_data.append(("test.fake.bbbbb", "foo"))
        multi_data.append(("test.fake.bbbbb1", "foo1"))
        do_set_multi_flag(multi_data)
        assert do_get_flag("test.fake.bbbbb") == "foo"
        assert do_get_flag("test.fake.bbbbb1") == "foo1"
