"""Test Constants for jwt."""
# pylint: disable=protected-access
import logging
import pytest
import ultron8
from ultron8.constants import jwt


logger = logging.getLogger(__name__)


@pytest.mark.constantsonly
@pytest.mark.unittest
class TestConstantsJWT(object):
    def test_constant_jwt(self) -> None:
        assert (
            jwt.JWT_REGEX
            == r"^{} [A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$"
        )
