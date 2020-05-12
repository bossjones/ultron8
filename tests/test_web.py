"""Test Web Module."""
# pylint: disable=protected-access
import logging
import os
import pytest

import ultron8

# from ultron8 import __version__
# from ultron8 import client
from ultron8.api import settings


logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def username_and_password_first_superuser_fixtures():
    yield settings.FIRST_SUPERUSER, settings.FIRST_SUPERUSER_PASSWORD


@pytest.mark.fastapionly
@pytest.mark.unittest
class TestFastAPIWeb:
    def test_fastapi_instance(
        self, mocker, username_and_password_first_superuser_fixtures, fastapi_client
    ):
        username, password = username_and_password_first_superuser_fixtures

        print(username)
        print(password)
        pass
