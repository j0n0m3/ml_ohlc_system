import json
from typing import Dict, List

from loguru import logger
from websocket import create_connection


class KrakenWebsocketTradeAPI:
    URL = 'wss://ws.kraken.com/v2'

    def __init__(
        self, 
        product_ids: List[str],
    ):
        self.product_ids = product_ids

        # establish connection to kraken ws api
        self._ws = create_connection(self.URL)
        logger.info('connection established')

        # subscribe to trades for given product_id
        self.subscribe(product_ids)

    def subscribe(self, product_ids: List[str]):
        """
        Establish connection to kraken ws api and subscribe to trades for given product_id
        """
        logger.info(f'subscribing to trades for {product_ids}')
        # subscribe to trades for given 'product_id'
        msg = {
            'method': 'subscribe',
            'params': {
                'channel': 'trade', 
                'symbol': product_ids, 
                'snapshot': False},
        }
        self._ws.send(json.dumps(msg))
        logger.info('subscribed')

        # dumping first two messages from ws api. contains no trade data, only connection confirmation
        for product_id in product_ids:
            _ = self._ws.recv()
            _ = self._ws.recv()

    def get_trades(self) -> List[Dict]:
        # mock_trades = [
        #     {
        #         'product_id': "BTC-USD",
        #         'price': 10000,
        #         'volume': 0.01,
        #         'timestamp': 163000000
        #     },
        #     {
        #         'product_id': "BTC-USD",
        #         'price': 10005,
        #         'volume': 0.01,
        #         'timestamp': 164000000
        #     }
        # ]

        message = self._ws.recv()

        if 'heartbeat' in message:
            # when heardbeat, return an empty list
            return []

        # parse message string as dict
        message = json.loads(message)

        # extract trade data from message['data']
        trades = []
        for trade in message['data']:
            trades.append(
                {
                    'product_id': trade['symbol'],
                    'price': trade['price'],
                    'volume': trade['qty'],
                    'timestamp': trade['timestamp'],
                }
            )

        # breakpoint()
        
        return trades
