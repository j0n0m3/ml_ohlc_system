import os
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings

# load .env file as env variables. access env variables using os.environ['VAR_NAME']
load_dotenv(find_dotenv())

# kafka_broker_address = os.environ['KAFKA_BROKER_ADDRESS']
# kafka_topic_name='trade'
# product_id = 'BTC/USD'

class Config(BaseSettings):
    product_id: str = 'ETH/USD'
    kafka_broker_address: str = os.environ['KAFKA_BROKER_ADDRESS']
    kafka_topic_name: str = 'trade'

config = Config()