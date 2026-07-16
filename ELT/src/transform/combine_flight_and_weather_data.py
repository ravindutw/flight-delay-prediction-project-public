from pyspark.sql import DataFrame
from pyspark.sql.types import *
import pyspark.sql.functions as F
from pyspark.sql.window import Window


def join_origin_weather_data(fd_df: DataFrame, wd_df: DataFrame, time_window) -> DataFrame:
    wd_df_prepd = _prep_wd_df(wd_df, 'origin')

    join_condition = [
        fd_df.ORIGIN == wd_df_prepd.station,
        wd_df_prepd.timestamp.between(
            fd_df.crs_departure_timestamp - time_window,
            fd_df.crs_departure_timestamp + time_window
        )
    ]

    joined_df = fd_df.join(wd_df_prepd, join_condition, 'left')

    joined_df = joined_df.withColumn(
        "time_diff_seconds",
        F.abs(F.unix_timestamp(fd_df.crs_departure_timestamp) - F.unix_timestamp(wd_df_prepd.timestamp))
    )

    window_spec = Window.partitionBy("flight_id").orderBy("time_diff_seconds")

    final_df = joined_df.withColumn("rn", F.row_number().over(window_spec)) \
        .filter(F.col("rn") == 1) \
        .drop("rn", "time_diff_seconds", "flights_id", "timestamp", 'station')

    return final_df



def join_destination_weather_data(fd_df: DataFrame, wd_df: DataFrame, time_window) -> DataFrame:
    wd_df_prepd = _prep_wd_df(wd_df, 'destination')

    join_condition = [
        fd_df.DEST == wd_df_prepd.station,
        wd_df_prepd.timestamp.between(
            fd_df.crs_arrival_timestamp - time_window,
            fd_df.crs_arrival_timestamp + time_window
        )
    ]

    joined_df = fd_df.join(wd_df_prepd, join_condition, 'left')

    joined_df = joined_df.withColumn(
        "time_diff_seconds",
        F.abs(F.unix_timestamp(fd_df.crs_arrival_timestamp) - F.unix_timestamp(wd_df_prepd.timestamp))
    )

    window_spec = Window.partitionBy("flight_id").orderBy("time_diff_seconds")

    final_df = joined_df.withColumn("rn", F.row_number().over(window_spec)) \
        .filter(F.col("rn") == 1) \
        .drop("rn", "time_diff_seconds", "flights_id", "timestamp", 'station')

    return final_df



def _prep_wd_df(wd_df: DataFrame, side: str):
    return wd_df.select(
        'station',
        'timestamp',
    
        F.col('air_temp_f').alias(f'{side}_air_temp_f'),
        F.col('dew_point_temp_f').alias(f'{side}_dew_point_temp_f'),
        F.col('relative_humidity').alias(f'{side}_relative_humidity'),
        F.col('wind_speed_kts').alias(f'{side}_wind_speed_kts'),
        F.col('wind_gust_kts').alias(f'{side}_wind_gust_kts'),
        F.col('visibility_miles').alias(f'{side}_visibility_miles'),
        F.col('sky_l1_coverage').alias(f'{side}_sky_l1_coverage'),
        F.col('1hr_precipitation_inches').alias(f'{side}_1hr_precipitation_inches'),
        F.col('pressure_altimeter_inches').alias(f'{side}_pressure_altimeter_inches')
    )