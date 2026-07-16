from pyspark.sql import DataFrame
from pyspark.sql.types import *
import pyspark.sql.functions as F

def create_utc_timestamps(fd_df: DataFrame) -> DataFrame:
    fd_df_ts = fd_df.withColumn(
        'crs_departure_timestamp_native',
        F.to_timestamp(F.concat_ws(' ', F.col('FL_DATE'), F.col('CRS_DEP_TIME')), "yyyy-MM-dd HH:mm")
    ).withColumn(
        'crs_departure_timestamp',
        F.to_utc_timestamp(F.col('crs_departure_timestamp_native'), F.col('origin_timezone'))
    ).withColumn(
        'departure_timestamp_native',
        F.to_timestamp(F.concat_ws(' ', F.col('FL_DATE'), F.col('DEP_TIME')), "yyyy-MM-dd HH:mm")
    ).withColumn(
        'departure_timestamp',
        F.to_utc_timestamp(F.col('departure_timestamp_native'), F.col('origin_timezone'))
    ).withColumn(
        'wheels_off_timestamp_native',
        F.to_timestamp(F.concat_ws(' ', F.col('FL_DATE'), F.col('WHEELS_OFF')), "yyyy-MM-dd HH:mm")
    ).withColumn(
        'wheels_off_timestamp',
        F.to_utc_timestamp(F.col('wheels_off_timestamp_native'), F.col('origin_timezone'))
    ).withColumn(
        'crs_arrival_timestamp_native',
        F.to_timestamp(F.concat_ws(' ', F.col('FL_DATE'), F.col('CRS_ARR_TIME')), "yyyy-MM-dd HH:mm")
    ).withColumn(
        'crs_arrival_timestamp',
        F.to_utc_timestamp(F.col('crs_arrival_timestamp_native'), F.col('destination_timezone'))
    ).withColumn(
        'arrival_timestamp_native',
        F.to_timestamp(F.concat_ws(' ', F.col('FL_DATE'), F.col('ARR_TIME')), "yyyy-MM-dd HH:mm")
    ).withColumn(
        'arrival_timestamp',
        F.to_utc_timestamp(F.col('arrival_timestamp_native'), F.col('destination_timezone'))
    ).withColumn(
        'wheels_on_timestamp_native',
        F.to_timestamp(F.concat_ws(' ', F.col('FL_DATE'), F.col('WHEELS_ON')), "yyyy-MM-dd HH:mm")
    ).withColumn(
        'wheels_on_timestamp',
        F.to_utc_timestamp(F.col('wheels_on_timestamp_native'), F.col('destination_timezone'))
    ).drop(
        'crs_departure_timestamp_native',
        'departure_timestamp_native',
        'wheels_off_timestamp_native',
        'crs_arrival_timestamp_native',
        'arrival_timestamp_native',
        'wheels_on_timestamp_native'
    ).withColumn(
        'flight_id',
        F.monotonically_increasing_id()
    )

    return fd_df_ts