from enum import Enum
from typing import List, Union
from urllib.parse import urlencode

import requests

from rumorz.enums import SearchMethod, EntityType, AssetClass, NodeMetrics, Lookback, ScreenerValues


class RumorzAPIException(Exception):
    pass


class RumorzClient:
    def __init__(self,
                 api_key,
                 api_url='https://prod-backend-rumorz-l2cw8.ondigitalocean.app'):
        self.api_url = api_url
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'X-API-Key': api_key
        }
        self._graph = self.Graph(self)
        self._agent = self.Agent(self)

    def _format_data(self, data):
        for key, value in data.items():
            if isinstance(value, Enum):
                data[key] = value.value

        todrop = []
        for key, value in data.items():
            if value is None:
                todrop.append(key)
        for key in todrop: data.pop(key)

    def post(self, endpoint, data):
        url = f"{self.api_url}/{endpoint}"
        self._format_data(data)
        response = requests.post(url, headers=self.headers, json=data)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise RumorzAPIException(response.json()['detail'])
        return response.json()

    def get(self, endpoint, data):
        url = f"{self.api_url}/{endpoint}"
        self._format_data(data)
        query_params_string = urlencode(data, doseq=True)
        # query_params_string = '%7B%27entities%27%3A%20%5B%7B%27type%27%3A%20%27financial_asset%27%2C%20%27name%27%3A%20%27Bitcoin%27%2C%20%27symbol%27%3A%20%27BTC%27%7D%5D%2C%20%27lookback%27%3A%20%277D%27%2C%20%27page%27%3A%201%2C%20%27limit%27%3A%2010%7D%0A'
        # query_params_string = "&".join([f"{k}={v}" for k, v in data.items() if v is not None])
        query_url = f"{url}?{query_params_string}"
        response = requests.get(query_url, headers=self.headers)
        response.text
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise RumorzAPIException(response.json()['detail'])
        return response.json()

    @property
    def graph(self):
        return self._graph

    @property
    def agent(self):
        return self._agent

    class Graph:
        def __init__(self, api):
            self.api = api

        def get_screener(self,
                         lookback: Union[str, Lookback] = None,
                         from_timestamp: str = None,
                         to_timestamp: str = None,
                         entity_type: Union[str, EntityType] = None):
            params = {
                "from_timestamp": from_timestamp,
                "to_timestamp": to_timestamp,
                "lookback": lookback,
                "entity_type": entity_type
            }
            return self.api.get('graph/screener', params)

        def get_posts(self,
                      type: Union[str, EntityType],
                      name: str,
                      symbol: str = None,
                      lookback: Union[str, Lookback] = None,
                      from_timestamp: str = None,
                      to_timestamp: str = None,
                      page: int = 1,
                      limit: int = 10):
            params = {
                "type": type,
                "name": name,
                "symbol": symbol,
                "lookback": lookback,
                "from_timestamp": from_timestamp,
                "to_timestamp": to_timestamp,
                "page": page,
                "limit": limit
            }
            return self.api.get('graph/posts', params)

        def get_time_series(self,
                            type: Union[str, EntityType],
                            name: str,
                            symbol: str = None,
                            lookback: Union[str, Lookback] = None,
                            from_timestamp: str = None,
                            to_timestamp: str = None,
                            page: int = 1,
                            limit: int = 10):
            params = {
                "type": type,
                "name": name,
                "symbol": symbol,
                "lookback": lookback,
                "from_timestamp": from_timestamp,
                "to_timestamp": to_timestamp,
                "page": page,
                "limit": limit
            }
            return self.api.get('graph/time-series', params)

    class Agent:
        def __init__(self, api):
            self.api = api
