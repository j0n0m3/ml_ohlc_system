from time import sleep
from typing import Dict, List

from kraken_api import KrakenWebsocketTradeAPI
from loguru import logger
from quixstreams import Application

from src.config import config
from src.kraken_api import KrakenWebsocketTradeAPI


def produce_trades(
    kafka_broker_address: str,
    kafka_topic_name: str,
    product_ids: List[str],
) -> None:
    """
    reads trades from Kraken ws api and saves into kafka topic

    args:
        kafka_broker_address (str): address of kafka broker
        kafka_topic (str): name of the kafka topic

    Returns:
        None
    """

    app = Application(broker_address=kafka_broker_address)

    # topic to save trades
    topic = app.topic(name=kafka_topic_name, value_serializer='json')

    logger.info(f'creating kraken api to fetch data for {product_ids}')

    # create kraken api instance
    kraken_api = KrakenWebsocketTradeAPI(product_ids=product_ids)

    logger.info('starting trade producer')

    # create producer instance
    with app.get_producer() as producer:
        while True:
            # get trades from kraken api
            trades: List[Dict] = kraken_api.get_trades()

            for trade in trades:
                # serialize event using definted Topic
                message = topic.serialize(key=trade['product_id'], value=trade)

                # produce message into kafka topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(trade)

            # slow down flow

            sleep(1)


if __name__ == '__main__':
    try:
        produce_trades(
            kafka_broker_address=config.kafka_broker_address,
            kafka_topic_name=config.kafka_topic_name,
            product_ids=config.product_ids,
        ) 
    except KeyboardInterrupt:
        logger.info('Exiting...')
