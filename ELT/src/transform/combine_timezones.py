from pyspark.sql import DataFrame
from pyspark.sql.types import *
import pyspark.sql.functions as F


def combine_flights_timezones(spark, fd_df, tz_df):
    fd_df.createOrReplaceTempView("flights")
    tz_df.createOrReplaceTempView("timezones")

    joined_df = spark.sql("""
        SELECT f.*, o.timezone AS origin_timezone, d.timezone AS destination_timezone
        FROM flights f 
        LEFT JOIN timezones o ON f.ORIGIN = o.iata_code
        LEFT JOIN timezones d ON f.DEST = d.iata_code
    """)

    return joined_df
