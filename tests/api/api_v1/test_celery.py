import pytest
import requests

from ultron8.api import settings

from tests.utils.utils import get_server_api


@pytest.mark.skip(reason="Celery is not fully implemented yet")
def test_celery_worker_test(superuser_token_headers):
    server_api = get_server_api()
    data = {"msg": "test"}
    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/utils/test-celery/",
        json=data,
        headers=superuser_token_headers,
    )
    response = r.json()
    assert response["msg"] == "Word received"
