"""
SonarrClient class
"""


from typing import Any

import requests


class SonarrClient:
    """
    SonarrClient class
    """

    def __init__(self, base_url: str = "", api_key: str = ""):
        """
        SonarrClient constructor

        :param base_url: Sonarr base URL
        :param api_key: Sonarr API key
        """
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "X-Api-Key": self.api_key
        }

    def get(self, endpoint: str, params: Any = None) -> Any:
        """
        Perform a GET request to Sonarr

        :param endpoint: Sonarr endpoint
        :param params: Request parameters

        :return: Response data
        """
        url = f"{self.base_url}/{endpoint}"

        response = requests.get(
            url=url, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {"status_code": response.status_code, "data": data}

    def post(self, endpoint: str, data: Any = None) -> Any:
        """
        Perform a POST request to Sonarr

        :param endpoint: Sonarr endpoint
        :param data: Request data

        :return: Response data
        """
        url = f"{self.base_url}/{endpoint}"

        response = requests.post(
            url=url, headers=self.headers, json=data, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {"status_code": response.status_code, "data": data}

    def put(self, endpoint: str, data: Any = None) -> Any:
        """
        Perform a PUT request to Sonarr

        :param endpoint: Sonarr endpoint
        :param data: Request data

        :return: Response data
        """
        url = f"{self.base_url}/{endpoint}"

        response = requests.put(
            url=url, headers=self.headers, json=data, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {"status_code": response.status_code, "data": data}

    def delete(self, endpoint: str) -> Any:
        """
        Perform a DELETE request to Sonarr

        :param endpoint: Sonarr endpoint

        :return: Response data
        """
        url = f"{self.base_url}/{endpoint}"

        response = requests.delete(url=url, headers=self.headers, timeout=10)
        response.raise_for_status()

        if response.status_code == 204:
            return {"status_code": response.status_code, "data": True}

        return {"status_code": response.status_code, "data": False}
