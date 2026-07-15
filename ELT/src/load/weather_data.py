import boto3
import gzip
from src.utils.config import load_config 
import pandas as pd
from src.utils.s3_paths import build_pandas_s3_data_lake_path, build_pandas_s3_data_warehouse_path


def write_to_datalake(raw_text: str, i):
    s3_bucket = cfg["aws"]["s3"]["data-lake-bucket"]
    s3_key = f"raw/Flight_Delay_Prediction_Datasets/weather_data/weather_batch_{i}.csv.gz"
    s3_client.put_object(
        Bucket=s3_bucket,
        Key=s3_key,
        Body=gzip.compress(raw_text.encode())
    )


def write_data_to_lake_csv(df, s3_key):
    s3_path = build_pandas_s3_data_lake_path(s3_key)
    df.to_csv(s3_path)


def write_data_to_lake_parquet(df, s3_key):
    s3_path = build_pandas_s3_data_lake_path(s3_key)
    df.to_parquet(s3_path, engine="pyarrow")


def get_lake_dataset(s3_key):
    s3_path = build_pandas_s3_data_lake_path(s3_key)
    return pd.read_csv(s3_path)


def get_warehouse_dataset(s3_key):
    s3_path = build_pandas_s3_data_warehouse_path(s3_key)
    return pd.read_csv(s3_path)