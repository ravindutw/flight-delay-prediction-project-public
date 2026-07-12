from .config import load_config


def build_spark_s3_data_lake_path(key):
    cfg = load_config()
    s3_bucket = cfg["aws"]["s3"]["data-lake-bucket"]

    return f"s3a://{s3_bucket}/{key}"


def build_spark_s3_data_warehouse_path(key):
    cfg = load_config()
    s3_bucket = cfg["aws"]["s3"]["data-warehouse-bucket"]

    return f"s3a://{s3_bucket}/{key}"


def build_pandas_s3_data_lake_path(key):
    cfg = load_config()
    s3_bucket = cfg["aws"]["s3"]["data-lake-bucket"]

    return f"s3://{s3_bucket}/{key}"


def build_pandas_s3_data_warehouse_path(key):
    cfg = load_config()
    s3_bucket = cfg["aws"]["s3"]["data-warehouse-bucket"]

    return f"s3://{s3_bucket}/{key}"