import os
from typing import List
from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

# load .env file as env variables. access env variables using os.environ['VAR_NAME']
load_dotenv(find_dotenv())

class Config(BaseSettings):
    kafka_broker_address: str = 'localhost:19092'
    kafka_topic_name: str = 'trade'
    product_ids: List[str] = [
        'ETH/USD',
        'BTC/USD',
        'ETH/EUR',
        'BTC/EUR',
        # 'BNB/USD',
        # 'SOL/USD',
    ]

    live_or_historical: str = 'live'
    last_n_days: int = 7

config = Config()