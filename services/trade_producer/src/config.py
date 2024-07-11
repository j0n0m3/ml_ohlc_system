import os
from dotenv import load_dotenv, find_dotenv

# load .env file as env variables. access env variables using os.environ['VAR_NAME']
load_dotenv(find_dotenv())

kafka_broker_address = os.environ['KAFKA_BROKER_ADDRESS']
kafka_topic_name='trade'
product_id = 'BTC/USD'