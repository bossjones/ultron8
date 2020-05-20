import logging

import requests

from tests.utils.utils import get_server_api
from ultron8.api import settings
import pytest

from typing import Dict
from ultron8.api.models.loggers import LoggerModel

logger = logging.getLogger(__name__)


@pytest.mark.convertingtotestclientstarlette
@pytest.mark.loggeronly
@pytest.mark.integration
class TestLoginApiEndpoint:
    def test_loggers_list(self, fastapi_client):
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)

        r = fastapi_client.get(f"{server_api}{settings.API_V1_STR}/logs")
        resp_json = r.json()
        assert r.status_code == 200

    def test_logger_get(self, fastapi_client):
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        # url = app.url_path_for("logger_get", logger_name=logger.name)
        r = fastapi_client.get(f"{server_api}{settings.API_V1_STR}/logs/{logger.name}")
        # response = client.get(url)
        assert r.status_code == 200
        assert r.json() == LoggerModel(name=logger.name, level=10, children=[])

    def test_logger_get_not_existing(self, fastapi_client):
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        r = fastapi_client.get(f"{server_api}{settings.API_V1_STR}/logs/wrong")
        assert r.status_code == 404

    def test_logger_patch(self, fastapi_client):
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        r = fastapi_client.patch(
            f"{server_api}{settings.API_V1_STR}/logs/",
            json={"name": logger.name, "level": "warning"},
        )
        assert r.status_code == 200
        logger.debug("should not be seen")
        assert logger.getEffectiveLevel() == 30
        assert r.json() == {"name": logger.name, "level": "warning"}

        # url = app.url_path_for("logger_patch")
        # response = client.patch(url, json={"name": logger.name, "level": "info"})
        # assert response.status_code == 200
        # logger.debug("should not be seen")
        # assert logger.getEffectiveLevel() == 20
        # assert response.json() == {"name": logger.name, "level": "info"}


# ok @wshayes I got a loggers.py in my router that looks like that
# https://gitter.im/tiangolo/fastapi?at=5ca3617fb34ccd69e7517360
# import logging

# from main import app
# from models.loggers import LoggerModel

# logger = logging.getLogger(__name__)


# def test_loggers_list(client):
#     url = app.url_path_for("loggers_list")
#     response = client.get(url)
#     assert response.status_code == 200


# def test_logger_get(client):
#     url = app.url_path_for("logger_get", logger_name=logger.name)
#     response = client.get(url)
#     assert response.status_code == 200
#     assert response.json() == LoggerModel(name=logger.name, level=30, children=[])


# def test_logger_get_not_existing(client):
#     url = app.url_path_for("logger_get", logger_name="wrong")
#     response = client.get(url)
#     assert response.status_code == 404


# def test_logger_patch(client):
#     url = app.url_path_for("logger_patch")
#     response = client.patch(url, json={"name": logger.name, "level": "info"})
#     assert response.status_code == 200
#     logger.debug("should not be seen")
#     assert logger.getEffectiveLevel() == 20
#     assert response.json() == {"name": logger.name, "level": "info"}


# def test_read_root_change_loggers(client, caplog):
#     messages_expected = [
#         ("warn message", 30),
#         ("error message", 40),
#         ("critical message", 50),
#         ("critical message", 50),
#         ("debug message", 10),
#         ("info message", 20),
#         ("warn message", 30),
#         ("error message", 40),
#         ("critical message", 50),
#     ]
#     url_logger_get_main = app.url_path_for("logger_get", logger_name="main")
#     response = client.get(url_logger_get_main)
#     assert response.status_code == 200
#     assert response.json() == LoggerModel(name="main", level=30, children=[])

#     url_root = app.url_path_for("read_root")
#     # by default as main logger level is not set it's on 20
#     response = client.get(url_root)
#     assert response.status_code == 200
#     # setting it to critical
#     urlpatch = app.url_path_for("logger_patch")
#     response = client.patch(urlpatch, json={"name": "main", "level": "critical"})
#     assert response.status_code == 200
#     assert response.json() == {"name": "main", "level": "critical"}
#     # checking what we see in logs once it has been hit
#     response = client.get(url_root)
#     assert response.status_code == 200
#     # setting it to debug
#     urlpatch = app.url_path_for("logger_patch")
#     response = client.patch(urlpatch, json={"name": "main", "level": "debug"})
#     assert response.status_code == 200
#     assert response.json() == {"name": "main", "level": "debug"}
#     # checking what we see in logs once it has been hit
#     response = client.get(url_root)
#     assert response.status_code == 200

#     # so now we should have 1) warn-error-critical 2)-critical 3)-debug-info-warn-error-critical
#     for check in zip(messages_expected, caplog.records):
#         assert check[0][0] == check[1].message
