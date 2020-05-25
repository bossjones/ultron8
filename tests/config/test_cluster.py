"""Test Cluster Configs."""
# pylint: disable=protected-access
import logging

import pytest
import requests
from starlette.testclient import TestClient

from ultron8.api import settings
import ultron8.config
from ultron8.config.cluster import ClusterConfig
from ultron8.config.manager import ConfigProxy, NullConfig, hash_digest
from ultron8.utils import maybe_decode, maybe_encode
from ultron8.yaml import yaml, yaml_load, yaml_save

from tests import helper
from tests.utils.utils import get_server_api

################################

# self, mocker: MockFixture, fastapi_client: TestClient, db: Session
logger = logging.getLogger(__name__)


@pytest.mark.configonly
@pytest.mark.unittest
class TestClusterConfig:
    def test_valid_ClusterConfig(self, fastapi_client: TestClient) -> None:
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        login_data = {
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        }
        r = fastapi_client.post(
            f"{server_api}{settings.API_V1_STR}/login/access-token", data=login_data
        )
        tokens = r.json()
        cluster_data = {
            "ultron_cluster_url": server_api,
            "ultron_acs_token": tokens["access_token"],
        }
        c = ClusterConfig(**cluster_data)

        assert c.ultron_cluster_url == "http://localhost:11267"
        assert c.ultron_acs_token
        assert c.ultron_uuid == "cd8f5f9f-e3e8-569f-87ef-f03c6cfc29bc"
        assert str(c) == f"http://localhost:11267{c.ultron_acs_token}"
