from quixstreams import Application
from loguru import logger
import json
from src.hopsworks_api import push_data_to_feature_store
from src.config import config

def kafka_to_feature_store(
        kafka_topic: str,
        kafka_broker_address: str,
        feature_group_name: str,
        feature_group_version: int,
) -> None:
    """
    reads 'ohlc' data from kafka topic and writes to feature store - writes data to feature group specified by 'feature_group_name' and 'feature_group_version'

    Args:
        kafka_topic (str): kafka topic to read ohlc data from
        kafka_broker_address (str): address of kafka broker
        feature_group_name (str): name of feature group to write data to
        feature_group_version (int): version of feature group to write data to

    Returns:
        None
    """
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group='kafka_to_feature_store',
    )    

    # create consumer and start polling loop
    with app.get_consumer() as consumer:
        consumer.subscribe(topics=[kafka_topic])

        while True:
            msg = consumer.poll(1)

            if msg is None:
                continue

            elif msg.error():
                logger.error('kafka error:', msg.error())

                # if message is an error, raise exception
                # raise Exception('kafka error:', msg.error())

                continue
            else:
                # data we need to send to feature store
                # step 1 - parse kafka message into dict
                ohlc = json.loads(msg.value().decode('utf-8'))
                
                # step 2 - write data to feature store
                push_data_to_feature_store(
                    feature_group_name=feature_group_name,
                    feature_group_version=feature_group_version,
                    data=ohlc,
                )

                # breakpoint()

            # store offset of processed message on consumer for auto-commit mechanism. will send to kafka in background. storing offset only after messaged is processed enables at-least-once delivery guarantees
            consumer.store_offsets(message=msg)

if __name__ == '__main__':
    kafka_to_feature_store(
        kafka_topic=config.kafka_topic,
        kafka_broker_address=config.kafka_broker_address,
        feature_group_name=config.feature_group_name,
        feature_group_version=config.feature_group_version,
    )