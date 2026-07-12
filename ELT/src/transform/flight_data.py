from pyspark.sql import DataFrame
import pyspark.sql.functions as F


def parse_fl_date(df: DataFrame, column: str = "FL_DATE") -> DataFrame:
    return df.withColumn(
        column,
        F.to_date(F.to_timestamp(F.col(column), "M/d/yyyy h:mm:ss a"))
    )


def correct_hhmm(df: DataFrame, column_names: list) -> DataFrame:
    for column_name in column_names:
        df = df.withColumn(column_name, F.lpad(F.col(column_name).cast("string"), 4, "0")).withColumn(column_name, F.when(F.col(column_name) == "2400", "0000").otherwise(F.col(column_name))).withColumn(column_name, F.date_format(F.to_timestamp(F.col(column_name), "HHmm"), "HH:mm"))
        
    return df


def drop_columns(df: DataFrame, columns: list[str]) -> DataFrame:
    return df.drop(*columns)


def fill_missing_values(df: DataFrame, columns: list[str], value=0) -> DataFrame:
    return df.fillna(value=value, subset=columns)


def drop_missing_values(df: DataFrame) -> DataFrame:
    return df.dropna()