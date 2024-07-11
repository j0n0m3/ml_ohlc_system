from typing import Dict, List

from kraken_api import KrakenWebsocketTradeAPI
from loguru import logger
from quixstreams import Application
from src import config


def produce_trades(
    kafka_broker_address: str,
    kafka_topic_name: str,
    product_id: str,
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

    # create kraken api instance
    kraken_api = KrakenWebsocketTradeAPI(product_id=product_id)

    logger.info('starting trade producer')
    # create producer instance
    with app.get_producer() as producer:
        while True:
            # get trades from kraken api
            trades: List[Dict] = kraken_api.get_trades()

            logger.info('got trades from kraken ws api')
            for trade in trades:
                # serialize event using definted Topic
                message = topic.serialize(key=trade['product_id'], value=trade)

                # produce message into kafka topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info('message sent!')

            # slow down flow
            from time import sleep

            sleep(1)


if __name__ == '__main__':
    produce_trades(kafka_broker_address=config.kafka_broker_address, kafka_topic_name=config.kafka_topic_name, product_id=config.product_id)
