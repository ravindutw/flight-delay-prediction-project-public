import pandas as pd
from src.utils.s3_paths import build_pandas_s3_data_lake_path


def rename_columns(df, new_column_names: dict):
    df.rename(columns=new_column_names, inplace=True)
    df.drop(columns=['Unnamed: 0'], inplace=True)
    return df


def timestamp_correction(df, column: str):
    df[column] = pd.to_datetime(df[column])
    return df


def type_corrections(df, column_name_1: str):
    df[column_name_1] = df[column_name_1].astype(str)
    return df
        