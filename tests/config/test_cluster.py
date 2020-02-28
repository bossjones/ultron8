"""Test Cluster Configs."""
# pylint: disable=protected-access
import logging
import hashlib
import os
import shutil
import tempfile
import unittest
import unittest.mock as mock
from pathlib import Path
from tempfile import mkdtemp
from tempfile import NamedTemporaryFile

import pytest

import ultron8.config
from tests import helper
from ultron8.yaml import yaml
from ultron8.yaml import yaml_load
from ultron8.yaml import yaml_save

from ultron8.utils import maybe_decode
from ultron8.utils import maybe_encode
from ultron8.config.manager import NullConfig
from ultron8.config.manager import ConfigProxy
from ultron8.config.manager import hash_digest


################################

import requests

from tests.utils.utils import get_server_api
from ultron8.api import settings
import pytest

from typing import Dict

from ultron8.config.cluster import ClusterConfig

logger = logging.getLogger(__name__)


@pytest.mark.configonly
@pytest.mark.unittest
class TestClusterConfig:
    def test_valid_ClusterConfig(self) -> None:
        server_api = get_server_api()
        logger.debug("server_api : %s", server_api)
        login_data = {
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        }
        r = requests.post(
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
