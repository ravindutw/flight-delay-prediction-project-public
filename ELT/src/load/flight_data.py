from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col
from src.utils.s3_paths import build_spark_s3_data_lake_path, build_spark_s3_data_warehouse_path


def write_extracted_data_to_lake(spark: SparkSession, df, s3_key):
    s3_path = build_spark_s3_data_lake_path(s3_key)
    df.coalesce(10).write.mode("overwrite").parquet(s3_path)


def write_transformed_data(spark: SparkSession, df, s3_key):
    s3_path = build_spark_s3_data_lake_path(s3_key)
    df.write.mode("overwrite").parquet(s3_path)


def get_flight_lake_dataset(spark: SparkSession, s3_key: str):
    s3_path = build_spark_s3_data_lake_path(s3_key)
    return spark.read.parquet(s3_path)


def get_warehouse_dataset(spark: SparkSession, s3_key: str):
    s3_path = build_spark_s3_data_warehouse_path(s3_key)
    return spark.read.parquet(s3_path)