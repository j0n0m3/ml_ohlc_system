import time
from time import sleep
from typing import Dict, List

from loguru import logger
from quixstreams import Application

from src.config import config
from src.kraken_api.websocket import KrakenWebsocketTradeAPI
from src.kraken_api.rest import KrakenRestAPI


def produce_trades(
    kafka_broker_address: str,
    kafka_topic_name: str,
    product_ids: List[str],
    live_or_historical: str,
    last_n_days: int,
) -> None:
    """
    reads trades from Kraken ws api and saves into kafka topic

    args:
        kafka_broker_address (str): address of kafka broker
        kafka_topic (str): name of the kafka topic
        product_ids (List[str]): list of product_ids for trades to be fetched
        live_or_historical (str): if historical, fetches trades from REST API
        last_n_days (int): numbers of days to fetch trades from REST API

    Returns:
        None
    """
    assert live_or_historical in {'live', 'historical'}, f'invalid value for live_or_historical: {live_or_historical}'

    app = Application(broker_address=kafka_broker_address)

    # topic to save trades
    topic = app.topic(name=kafka_topic_name, value_serializer='json')

    logger.info(f'creating kraken api to fetch data for {product_ids}')

    # create kraken api instance
    if live_or_historical == 'live':
        kraken_api = KrakenWebsocketTradeAPI(product_ids=product_ids)
    else:
        # get current timestamp in ms
        to_ms = int(time.time() * 1000)
        from_ms = to_ms - last_n_days * 24 * 60 * 60 * 1000

        kraken_api = KrakenRestAPI(product_ids=product_ids, 
                                   from_ms=from_ms, 
                                   to_ms=to_ms)

    logger.info('creating producer')

    # create producer instance
    with app.get_producer() as producer:
        while True:

            #check if done fetching historical data
            if kraken_api.is_done():
                logger.info('done fetching historical data')
                break

            # get trades from kraken api
            trades: List[Dict] = kraken_api.get_trades()

            for trade in trades:
                # serialize event using definted Topic
                message = topic.serialize(key=trade['product_id'], value=trade)

                # produce message into kafka topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(trade)

            # slow down flow

            # sleep(1)


if __name__ == '__main__':
    try:
        produce_trades(
            kafka_broker_address=config.kafka_broker_address,
            kafka_topic_name=config.kafka_topic_name,
            product_ids=config.product_ids,

            # params needed when running trade_producer agaisnt historical data from REST API
            live_or_historical=config.live_or_historical,
            last_n_days=config.last_n_days,
        ) 
    except KeyboardInterrupt:
        logger.info('Exiting...')
