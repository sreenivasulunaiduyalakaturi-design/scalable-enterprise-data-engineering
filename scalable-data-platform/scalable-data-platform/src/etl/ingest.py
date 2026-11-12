"""Bronze layer: land raw data as-is (plus audit columns) in columnar format."""
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import (StructType, StructField, LongType, StringType,
                               IntegerType, DoubleType)

RAW_SCHEMA = StructType([
    StructField("order_id", LongType()),
    StructField("customer_id", StringType()),
    StructField("category", StringType()),
    StructField("quantity", IntegerType()),
    StructField("unit_price", DoubleType()),
    StructField("order_date", StringType()),
])


def run(spark: SparkSession, cfg: dict):
    df = (spark.read.option("header", True).schema(RAW_SCHEMA).csv(cfg["paths"]["raw"])
          .withColumn("_ingested_at", F.current_timestamp())
          .withColumn("_source_file", F.input_file_name()))
    df.write.mode("overwrite").parquet(cfg["paths"]["bronze"])
    return df.count()
