import requests
import json
from typing import List, Dict

from loguru import logger

class KrakenRestAPI:

    URL = 'https://api.kraken.com/0/public/Trades?pair={product_id}&since={since_ms}'

    def __init__ (
        self,
        product_ids: List[str],
        from_ms: int,
        to_ms: int,
    ) -> None:
        '''
        initialization of kraken rest api

        args:
            product_ids (List[str]): list of product_ids for which trades to be fetched
            from_ms (int): start timestamp in ms
            to_ms (int): end timestamp in ms

        returns:
            None
        '''
        self.product_ids = product_ids
        self.from_ms = from_ms
        self.to_ms = to_ms

    def get_trades(self) -> List[Dict]:
        '''
        fetches batch of trades from kraken rest api and returns list of dict

        args:
            none

        returns:
            List[Dict]: list of dict where each dict represents a trade
        '''
        payload = {}
        headers = {'Accept': 'application/json'}
        
        # replacing placeholder in URL with values for product_id and since_ms
        url = self.URL.format(product_id=self.product_ids[0], since_ms=self.from_ms)
        
        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)

        data = json.loads(response.text)

        breakpoint()

    def is_done(self) -> bool:
        return False