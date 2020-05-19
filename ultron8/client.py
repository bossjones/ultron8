# pylint: disable=logging-not-lazy
import os
import logging
import time
import datetime
from contextlib import contextmanager
import collections.abc as abc_collections
import dateutil.parser
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry  # pylint: disable=import-error

from ultron8.api import settings
from ultron8 import __version__
from ultron8.u8client.utils import get_api_endpoint
from ultron8.constants import media_types
from ultron8.api.models.user import UserCreate

logger = logging.getLogger(__name__)

# def get_api_endpoint() -> str:
#     server_name = f"http://{settings.SERVER_NAME}"
#     logger.debug("server_name: '%s'", server_name)
#     return server_name


class UltronAPI:
    # def __init__(self, base_url=None, auth_url=None, api_url=None, stream_url=None,
    # api_version=None, cacert=None, debug=False, token=None, api_key=None):
    def __init__(self, api_endpoint=None, jwt_token=None):
        # assert len(jwt_token) > 39

        # Get CLI options. If not given, then try to get it from the environment.
        self.endpoints = dict()

        if api_endpoint:
            self.api_endpoint = api_endpoint.rstrip("/")
        else:
            self.api_endpoint = get_api_endpoint()

        self.endpoints["base"] = self.api_endpoint

        self.api_url = f"{self.api_endpoint}{settings.API_V1_STR}"

        self.endpoints["api"] = f"{self.api_endpoint}{settings.API_V1_STR}"
        self.endpoints["login"] = f"{self.api_endpoint}{settings.API_V1_STR}/login"
        self.endpoints["logs"] = f"{self.api_endpoint}{settings.API_V1_STR}/logs"
        self.endpoints["token"] = f"{self.api_endpoint}{settings.API_V1_STR}/token"
        self.endpoints["home"] = f"{self.api_endpoint}{settings.API_V1_STR}/"
        self.endpoints["alive"] = f"{self.api_endpoint}{settings.API_V1_STR}/alive"
        self.endpoints["version"] = f"{self.api_endpoint}{settings.API_V1_STR}/version"
        self.endpoints["users"] = f"{self.api_endpoint}{settings.API_V1_STR}/users"
        self.endpoints["items"] = f"{self.api_endpoint}{settings.API_V1_STR}/items"
        self.endpoints["metrics"] = f"{self.api_endpoint}{settings.API_V1_STR}/metrics"

        if jwt_token:
            self.jwt_token = jwt_token
        else:
            self.jwt_token = None

    def _update_endpoints(self):
        logger.debug("Refreshing client endpoints ....")
        self.endpoints["base"] = self.api_endpoint
        self.api_url = f"{self.api_endpoint}{settings.API_V1_STR}"
        self.endpoints["api"] = f"{self.api_url}"
        self.endpoints["login"] = f"{self.api_url}/login"
        self.endpoints["logs"] = f"{self.api_url}/logs"
        self.endpoints["token"] = f"{self.api_url}/token"
        self.endpoints["home"] = f"{self.api_url}/"
        self.endpoints["alive"] = f"{self.api_url}/alive"
        self.endpoints["version"] = f"{self.api_url}/version"
        self.endpoints["users"] = f"{self.api_url}/users"
        self.endpoints["items"] = f"{self.api_url}/items"
        self.endpoints["metrics"] = f"{self.api_url}/metrics"
        logger.debug("Client endpoints refreshed....")

    def set_api_endpoint(self, v):
        logger.debug("Old api_endpoint: {}".format(self.api_endpoint))
        self.api_endpoint = v.rstrip("/")
        self._update_endpoints()
        logger.debug("New api_endpoint: {}".format(self.api_endpoint))

    def _headers(self) -> dict:
        return {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
        }

    def _retry_requests(self, url, total=5, backoff=1, **kwargs):
        s = requests.Session()
        retries = Retry(
            total=total, backoff_factor=backoff, status_forcelist=[502, 503, 504]
        )
        s.mount("http://", HTTPAdapter(max_retries=retries))

        return s.get(url, **kwargs)

    # FYI, borrowed from k8s-migration-tooling
    def _get_logger(self, logger_name: str):
        url = f"{self.endpoints['logs']}/{logger_name}"
        logger.debug("Ultron8 get envs API URL : " + url)
        header_debug = self._headers()
        logger.debug("Token preview:" + header_debug["Authorization"][-4:])
        r = self._retry_requests(url, headers=self._headers())
        if r.text is not None:
            logger.debug(r.text)
        if r.status_code != 200:
            logger.debug(f"_get_logger returned {r.status_code} {r.json()} {url}")
            raise AssertionError("Failed to get Loggers")

        return r.json()

    # FYI, borrowed from k8s-migration-tooling
    def _get_version(self):
        url = f"{self.endpoints['version']}"
        logger.debug("Ultron8 get version URL : " + url)
        header_debug = self._headers()
        logger.debug("Token preview:" + header_debug["Authorization"][-4:])
        r = self._retry_requests(url, headers=self._headers())
        if r.text is not None:
            logger.debug(r.text)
        if r.status_code != 200:
            logger.debug(f"_get_version returned {r.status_code} {r.json()} {url}")
            raise AssertionError("Failed to get Version")

        return r.json()

    def _get_alive(self):
        url = f"{self.endpoints['alive']}"
        logger.debug("Ultron8 get alive URL : " + url)
        header_debug = self._headers()
        logger.debug("Token preview:" + header_debug["Authorization"][-4:])
        r = self._retry_requests(url, headers=self._headers())
        if r.text is not None:
            logger.debug(r.text)
        if r.status_code != 200:
            logger.debug(f"_get_alive returned {r.status_code} {r.json()} {url}")
            raise AssertionError("Failed to get alive")

        return r.json()

    def _get_users(self):
        url = f"{self.endpoints['users']}"
        logger.debug("Ultron8 get users URL : " + url)
        header_debug = self._headers()
        logger.debug("Token preview:" + header_debug["Authorization"][-4:])
        r = self._retry_requests(url, headers=self._headers())
        if r.text is not None:
            logger.debug(r.text)
        if r.status_code != 200:
            logger.debug(f"_get_users returned {r.status_code} {r.json()} {url}")
            raise AssertionError("Failed to get users")

        return r.json()

    # FYI, borrowed from k8s-migration-tooling
    def _post_login_access_token(self, username: str, password: str):
        url = f"{self.endpoints['login']}/access-token"
        print("Ultron8 post login accesss-token URL : " + url)

        data = {
            "username": username,
            "password": password,
        }

        r = requests.post(url, data=data)

        if r.status_code != 200:
            print(f"_post_login_access_token returned {r.status_code} {r.json()} {url}")
            raise AssertionError("Failed to get new access token")

        tokens = r.json()
        # a_token = tokens["access_token"]
        # headers = {"Authorization": f"Bearer {a_token}"}
        return tokens

    def _get_metrics(self):
        # Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
        url = f"{self.endpoints['metrics']}"
        logger.debug("Ultron8 get metrics URL : " + url)
        header_debug = {
            "accept": media_types.TEXT_TYPE,
            "Authorization": f"Bearer {self.jwt_token}",
        }
        logger.debug("Token preview:" + header_debug["Authorization"][-4:])
        r = self._retry_requests(url, headers=self._headers())
        if r.text is not None:
            logger.debug(r.text)
        if r.status_code != 200:
            logger.debug(f"_get_metrics returned {r.status_code} {r.json()} {url}")
            raise AssertionError("Failed to get metrics")

        return r.text

    # FYI, borrowed from k8s-migration-tooling
    def _post_create_user(self, data: dict):
        url = f"{self.endpoints['users']}/"

        headers = self._headers()

        # data = UserCreate(
        #     email=data["email"],
        #     password=data["password"]
        # )

        # data["id"] = None

        r = requests.post(url, data=data, headers=headers)

        if r.status_code != 200:
            print(f"_post_login_access_token returned {r.status_code} {r.json()} {url}")
            raise AssertionError("Failed to get new access token")

        tokens = r.json()
        return tokens
