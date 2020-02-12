import logging
import requests
from typing import Optional, List

from morningstar.models.ms_response import MSResponse
from morningstar.models.ts_response import TSResponse
from morningstar.provider.provider import Provider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Morningstar(Provider):
    """Morningstar API

    Note:
        This class combines multiple endpoints:
            - http://msuxml.morningstar.com/IndexTS
            - http://msxml.tenfore.com/search
            - http://msxml.tenfore.com/index.php

    Attributes:
        credentials (dict): Provider specific configuration including "username" and "password"
    """

    def __init__(self, config):
        super().__init__(config)

    def _build_url(self, base: str, params: dict, params_arr: Optional[list]):
        url_params = ''.join(['&{}={}'.format(k, v) for k, v in params.items()])
        if params_arr:
            url_params_arr = ''.join(['&{}'.format(p) for p in params_arr])
        else:
            url_params_arr = ''
        url = base + \
              '?username={}&password={}'.format(self.config['username'], self.config['password']) + \
              url_params + url_params_arr
        return url + '&json'

    def _request(self, base: str, params: dict, params_arr: list):
        response = requests.get(self._build_url(base=base,
            params=params, params_arr=params_arr))
        return response.json()

    def _tenfore(self, endpoint: str, params: dict, params_arr: Optional[list] = None):
        base = 'http://msxml.tenfore.com/{}'.format(endpoint)
        return self._request(base=base, params=params, params_arr=params_arr)

    def _morningstar(self, endpoint: str, params: dict, params_arr: Optional[list] = None):
        base = 'http://msuxml.morningstar.com/{}'.format(endpoint)
        return self._request(base=base, params=params, params_arr=params_arr)

    def search(self, params: dict):
        """Search endpoint

        Args:
            params (dict): e.g. {"isin": "US46625H1005"}

        Returns:

        """
        response = self._tenfore('search', params)
        return MSResponse.from_dict(response)

    def index(self, params: dict):
        """Index endpoint

        Args:
            params (dict): e.g. {"isin": "US46625H1005"}

        Returns:

        """
        response = self._tenfore('index.php', params)
        return MSResponse.from_dict(response)

    def index_ts(self, params: dict, params_arr: list = []):
        """IndexTS endpoint

        Args:
            params (dict): e.g. {"isin": "US46625H1005"}

        Returns:

        """
        response = self._morningstar('IndexTS', params)
        return TSResponse.from_dict(response)
