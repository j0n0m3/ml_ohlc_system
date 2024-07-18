from datetime import timedelta
from loguru import logger
from quixstreams import Application


def trade_to_ohlc(
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_broker_address: str,
    ohlc_window_seconds: int,
) -> None:
    """
    reads trade data from kafka_input_topic, aggregates into OHLC data with given window size, and writes OHLC data to kafka_output_topic

    Args:
        kafka_input_topic (str): kafka topic to read trade data from
        kafka_output_topic (str): kafka topic to write OHLC data to
        kafkfa_broker_address (str): kafka broker address
        ohlc_window_seconds (int): window size in seconds for OHLC aggregation 

    Returns:
        None
    """

    # hands all low level comms with kafka
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group="trade_to_ohlc",
        auto_offset_reset="earliest" # process all messages from beginning
        # auto_create_reset="latest" # ignore previous, only use new messages coming from this moment
    )

    # specify input and output topics for app
    input_topic = app.topic(name=kafka_input_topic, value_serializer='json')
    output_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    # create streaming df to apply transformations to incoming data
    sdf = app.dataframe(topic=input_topic)
   
    def init_ohlc_candle(value: dict) -> dict:
        """
        initialize OHLC with first trade data
        """
        return {
            "open": value['price'],
            "high": value['price'],
            "low": value['price'],
            "close": value['price'],
            "product_id": value['product_id']
        }
    
    def update_ohlc_candle(ohlc_candle: dict, trade: dict) -> dict:
        """
        update OHLC data with incoming trade data

        args:
            ohlc: dict: current OHLC candle
            value: dict: incoming trade data

        returns:
            dict: update ohlc candle
        """
        return{
            "open": ohlc_candle['open'],
            "high": max(ohlc_candle['high'], trade['price']),
            "low": min(ohlc_candle['low'], trade['price']),
            "close": trade['price'],
            "product_id": trade['product_id'],
        }

    # START: apply transformations to incoming data. applying tumbling windows to transform incoming messages into OHLC data
    sdf = sdf.tumbling_window(duration_ms=timedelta(seconds=ohlc_window_seconds))
    sdf = sdf.reduce(reducer=update_ohlc_candle, initializer=init_ohlc_candle).current()

    # extract open, high, low, close from values. current format is: {'start': 1620000000000, 'end': 1620000001000, 'value': {'open': 100, 'high': 110, 'low': 90, 'close': 105}
    # msg format we need: {'timestamp': 1620000000000 (end of window), 'open': 100, 'high': 110, 'low': 90, 'close': 105, 'product_id': 'ETH/USD'}
    
    # unpacking values we want
    sdf['open'] = sdf['value']['open']
    sdf['high'] = sdf['value']['high']
    sdf['low'] = sdf['value']['low']
    sdf['close'] = sdf['value']['close']
    sdf['product_id'] = sdf['value']['product_id']

    # adding timestamp key
    sdf['timestamp'] = sdf['end']

    # lets keep only keys we want in final message
    sdf = sdf[['timestamp', 'open', 'high', 'low', 'close', 'product_id']]
    
    # END: apply transformations to incoming data

    sdf = sdf.update(logger.info)

    sdf = sdf.to_topic(output_topic)

    # initiate streaming application
    app.run(sdf)

if __name__ == '__main__':

    from src.config import config

    trade_to_ohlc(
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_broker_address=config.kafka_broker_address,
        ohlc_window_seconds=config.ohlc_window_seconds,
    )