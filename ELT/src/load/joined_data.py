from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col
from src.utils.s3_paths import build_spark_s3_data_lake_path, build_spark_s3_data_warehouse_path


def write_to_data_warehouse(spark: SparkSession, df, s3_key):
    s3_path = build_spark_s3_data_warehouse_path(s3_key)
    df.write.mode("overwrite").parquet(s3_path)