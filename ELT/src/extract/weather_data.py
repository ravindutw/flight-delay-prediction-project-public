import pandas as pd
import boto3
import os
import gzip
from src.utils.config import load_config 

def _load_raw_weather_data():
    cfg = load_config()
    s3_bucket = cfg["aws"]["s3"]["data-lake-bucket"]
    s3_prefix = 'raw/Flight_Delay_Prediction_Datasets/weather_data/'

    s3_client = boto3.client('s3')
    session = boto3.Session()
    s3 = session.resource('s3')
    bucket = s3.Bucket(s3_bucket)

    paginator = s3_client.get_paginator("list_objects_v2")

    file_list = []
    
    for page in paginator.paginate(Bucket=s3_bucket, Prefix=s3_prefix):
        for obj in page.get("Contents", []):
            if obj["Key"].endswith("csv.gz"):
                file_list.append(obj["Key"])

    return file_list, bucket


def concat_weather_data():
    file_list, bucket = _load_raw_weather_data()

    df_combined = pd.concat(
        (pd.read_csv(bucket.Object(f).get()["Body"], compression="gzip") for f in file_list),
        ignore_index=True
    )

    return df_combined