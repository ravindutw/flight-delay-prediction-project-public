import os
from pyspark.sql import SparkSession
from .config import load_config
from src.utils.logging_setup import setup_file_logging

def get_spark_session() -> SparkSession:
    cfg = load_config()
    spark_cfg = cfg["spark"]
    
    if "local_ip" in spark_cfg:
        os.environ["SPARK_LOCAL_IP"] = spark_cfg["local_ip"]

    builder = (
        SparkSession.builder
        .appName(spark_cfg["app_name"])
        .config("spark.sql.shuffle.partitions", spark_cfg.get("shuffle_partitions", 200))
        .config("spark.driver.extraJavaOptions", "-Dlog4j.configurationFile=file:config/log4j2.properties")
    )

    if spark_cfg.get("jars_packages"):
        builder = builder.config("spark.jars.packages", ",".join(spark_cfg["jars_packages"]))

    for key, value in spark_cfg.get("hadoop_conf", {}).items():
        builder = builder.config(f"spark.hadoop.{key}", value)

    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel(spark_cfg.get("log_level", "WARN"))
    return spark