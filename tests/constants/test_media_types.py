"""Test Constants for media_types."""
# pylint: disable=protected-access
import logging

import pytest

import ultron8
from ultron8.constants import media_types

logger = logging.getLogger(__name__)


@pytest.mark.constantsonly
@pytest.mark.unittest
class TestConstantsMediaTypes(object):
    def test_constant_media_types(self) -> None:
        assert media_types.JSON_TYPE == "application/json"
        assert media_types.TEXT_TYPE == "text/plain; charset=utf-8"
        assert media_types.HTML_TYPE == "text/html; charset=utf-8"
        assert media_types.OVERRIDE_TYPE == "application/x-override"
