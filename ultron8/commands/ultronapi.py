# import requests
# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.util.retry import Retry  # pylint: disable=import-error


# class UltronAPI:
#     def __init__(self, api_endpoint: str, jwt_token: str):
#         assert len(jwt_token) > 39
#         self.api_endpoint = api_endpoint.rstrip("/")
#         self.jwt_token = jwt_token

#     def _headers(self) -> dict:
#         return {
#             "accept": "application/json",
#             "Authorization": f"token {self.jwt_token}",
#         }

#     def _retry_requests(self, url, total=5, backoff=1, **kwargs):
#         s = requests.Session()
#         retries = Retry(
#             total=total, backoff_factor=backoff, status_forcelist=[502, 503, 504]
#         )
#         s.mount("http://", HTTPAdapter(max_retries=retries))

#         return s.get(url, **kwargs)

#     def _get_environments(self, product_name: str, service_name: str):
#         url = f"{self.api_endpoint}/v1/{product_name}/{service_name}/environments"
#         print("Moonbeam get envs API URL : " + url)
#         header_debug = self._headers()
#         print("Token preview:" + header_debug["Authorization"][-4:])
#         r = self._retry_requests(url, headers=self._headers())
#         if r.text is not None:
#             print(r.text)
#         if r.status_code != 200:
#             print(f"_get_environments returned {r.status_code} {r.json()} {url}")
#             raise AssertionError("Failed to get environments")

#         return r.json()["environments"]

#     def _post_projects(
#         self,
#         product_name: str,
#         service_name: str,
#         environment_id: int,
#         environment_stage_id: int,
#         project_group_id: int,
#         title: str,
#         name: str,
#         lambda_config_id: int,
#     ):
#         url = f"{self.api_endpoint}/v1/{product_name}/{service_name}/environments/{environment_id}/environment_stages/{environment_stage_id}/projects"

#         data = {
#             "project[name]": name,
#             "project[title]": title,
#             "project[project_group_id]": project_group_id,
#             "project[build_configuration_type]": "lambda",
#             "project[build_configuration_id]": lambda_config_id,
#             "project[required]": True,
#             "project[deploy_token]": True,
#             "project[rollback]": True,
#             "project[unstable_allowed]": True,
#         }

#         r = requests.post(url, headers=self._headers(), data=data)

#         if r.status_code != 201:
#             print(f"_post_projects returned {r.status_code} {r.json()} {url}")
#             raise AssertionError("Failed to post project")

#         return r.json()
