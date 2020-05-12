"""Test Web Module."""
# pylint: disable=protected-access
import logging
import os
import pytest

import ultron8

# from ultron8 import __version__
# from ultron8 import client
from ultron8.api import settings
from tests.utils.utils import get_server_api_with_version


logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def username_and_password_first_superuser_fixtures():
    yield settings.FIRST_SUPERUSER, settings.FIRST_SUPERUSER_PASSWORD


@pytest.mark.fastapionly
@pytest.mark.unittest
class TestFastAPIWeb:
    def test_fastapi_instance(self, mocker, fastapi_client):
        # username, password = username_and_password_first_superuser_fixtures
        url = "{base}/logs".format(base=get_server_api_with_version())
        response = fastapi_client.get(url)
        assert response.status_code == 200

    # def test_fastapi_instance_routes(
    #     self, mocker, fastapi_client
    # ):
    #     # username, password = username_and_password_first_superuser_fixtures
    #     url = "{base}/logs".format(base=get_server_api_with_version())
    #     response = fastapi_client.get(url)
    #     assert response.status_code == 200
