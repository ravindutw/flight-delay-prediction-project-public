import pandas as pd
from pyspark.sql import SparkSession
from src.utils.s3_paths import build_pandas_s3_data_lake_path, build_pandas_s3_data_warehouse_path, build_spark_s3_data_lake_path

def write_data_to_lake_parquet(df, s3_key):
    s3_path = build_pandas_s3_data_lake_path(s3_key)
    df.to_parquet(s3_path, engine="pyarrow")


def get_tz_lake_dataset(spark: SparkSession, s3_key: str):
    s3_path = build_spark_s3_data_lake_path(s3_key)
    return spark.read.parquet(s3_path)