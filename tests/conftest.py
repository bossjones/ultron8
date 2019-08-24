# Taken from tedi and guid_tracker
import datetime
import os
from pathlib import Path

import pytest
from starlette.testclient import TestClient

from tests.utils.utils import get_server_api
from tests.utils.utils import get_superuser_token_headers

# from ultron8.api import settings
# from ultron8.web import app

from typing import Dict

here = os.path.abspath(os.path.dirname(__file__))

print("here: {}".format(here))

# fixtures_path = Path('ultron8/tests/fixtures').resolve()
fixtures_path = Path("tests/fixtures").resolve()


FAKE_TIME = datetime.datetime(2020, 12, 25, 17, 5, 55)


@pytest.fixture(scope="module")
def server_api():
    return get_server_api()


@pytest.fixture(scope="module")
def superuser_token_headers() -> Dict[str, str]:
    return get_superuser_token_headers()


# @pytest.fixture()
# def client():
#     """
#     When using the 'client' fixture in test cases, we'll get full database
#     rollbacks between test cases:
#     def test_homepage(client):
#         url = app.url_path_for('homepage')
#         response = client.get(url)
#         assert response.status_code == 200
#     """
#     client = TestClient(app)
#     with TestClient(app) as client:
#         yield client


@pytest.fixture
def patch_datetime_now(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls):
            return FAKE_TIME

    monkeypatch.setattr(datetime, "datetime", mydatetime)
