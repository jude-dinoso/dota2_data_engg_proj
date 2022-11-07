import json
from typing import Optional

import requests

API_URL = "https://api.opendota.com/api/"


class APIException(Exception):
    pass


class OpenDota2API:
    API_URL = "https://api.opendota.com/api/"

    def get_heroes_list(self) -> list[str]:
        api_url = self.API_URL + "heroes"
        response = self.call_api("GET", api_url)
        return json.loads(response.text)

    def get_public_match_data(self, **kwargs) -> list[str]:
        if not kwargs:
            kwargs = {"mmr_descending": 60}
        api_url = self.API_URL + "publicMatches"
        query_params = kwargs
        response = self.call_api("GET", api_url, query_params)
        return json.loads(response.text)

    def get_match_data(self, **kwargs) -> list[str]:
        if not kwargs:
            return []
        api_url = self.API_URL + "matches" + kwargs.get("match_id", "")
        response = self.call_api("GET", api_url)
        return json.loads(response.text)

    @staticmethod
    def call_api(method, api_url: str, query_params=None) -> Optional:
        response = requests.request(method=method, url=api_url, params=query_params)
        if response.status_code == 200:
            return response
        else:
            raise APIException("API Exception")
