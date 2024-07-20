import hopsworks
import pandas as pd
from src.config import config

def push_data_to_feature_store(
        feature_group_name: str,
        feature_group_version: int,
        data: dict,
) -> None:
    """
    pushes given 'data' to feature store, writing to feature group with name 'feature_group_name' and version 'feature_group_version'

    Args:
        feature_group_name (str): name of feature group to write data to
        feature_group_version (int): version of feature group to write data to
        data (dict): data to write to feature store

    Returns:
        None
    """
    
    # auth with hopsworks api/project
    project = hopsworks.login(
        project=config.hopsworks_project_name,
        api_key_value=config.hopsworks_api_key,
    )

    # get feature store handle
    feature_store = project.get_feature_store()

    # get/create feature group - saving feature data to
    ohlc_feature_group = feature_store.get_or_create_feature_group(
        name=feature_group_name,
        version=feature_group_version,
        description='OHLC data from websocket',
        primary_key=['product_id', 'timestamp'],
        event_time='timestamp',
        online_enabled=True,
    )

    # breakpoint()

    # transform data (dict) into pandas dataframe
    data = pd.DataFrame([data])

    # write data to feature group
    ohlc_feature_group.insert(data)