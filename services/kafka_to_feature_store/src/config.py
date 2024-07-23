import os
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings

# load .env file as env variables. access env variables using os.environ['VAR_NAME']
load_dotenv(find_dotenv())

class Config(BaseSettings):

    kafka_broker_address: str = 'locahost:19092'
    kafka_topic: str
    feature_group_name: str
    feature_group_version: int
    hopsworks_project_name: str = os.environ['HOPSWORKS_PROJECT_NAME']
    hopsworks_api_key: str = os.environ['HOPSWORKS_API_KEY']

config = Config()