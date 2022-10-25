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
        response = self.call_api(api_url)
        return json.loads(response.text)

    @staticmethod
    def call_api(api_url: str, query_params=None) -> Optional:
        response = requests.get(api_url, params=query_params)
        if response.status_code == 200:
            return response
        else:
            raise APIException("API Exception")
