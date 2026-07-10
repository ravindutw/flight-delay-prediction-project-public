from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col
from functools import reduce
from pyspark.sql import DataFrame
from src.utils.s3_paths import build_spark_s3_data_lake_path

def extract_flight_data(spark: SparkSession):
    data_file_names = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    s3_key = "raw/Flight_Delay_Prediction_Datasets/flight_data"
    s3_base_path = build_spark_s3_data_lake_path(s3_key)

    dfs = [
        spark.read.csv(
            f"{s3_base_path}/{f}.csv", 
            header=True,
            inferSchema=True
        ) 
        for f in data_file_names
    ]

    combined_df = reduce(DataFrame.union, dfs)
    return combined_df
    