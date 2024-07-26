import os
from dotenv import load_dotenv, find_dotenv

# load .env file as env variables. access env variables using os. environ['VAR_NAME']
load_dotenv(find_dotenv())

from pydantic_settings import BaseSettings

class Config(BaseSettings):
    kafka_broker_address: str = 'localhost:19092'
    kafka_input_topic: str = 'trade'
    kafka_output_topic: str = 'ohlc'
    ohlc_window_seconds: int

config = Config()