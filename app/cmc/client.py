from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json, os
from typing import Dict, Optional

BASE_URL = "https://pro-api.coinmarketcap.com"


class CoinMarketCapClient:
    def __init__(self):
        self.base_url = BASE_URL

    def get_categories(self) -> Optional[Dict]:
        '''
        Returns information about all coin categories available on CoinMarketCap.
        Includes a paginated list of cryptocurrency quotes and metadata from each category.
        :return:
        '''
        url = self.base_url + "/v1/cryptocurrency/categories"

        parameters = {
            'start': '1',
            'limit': '5000'
        }

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': os.environ['CMC_KEY'],
            # 'X-CMC_PRO_API_KEY': ,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            return data
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
            return None


cmc_client = CoinMarketCapClient()
