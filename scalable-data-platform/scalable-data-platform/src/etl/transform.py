"""Silver layer: clean, validate, deduplicate, enrich."""
from pyspark.sql import DataFrame, SparkSession, functions as F


def clean(df: DataFrame) -> DataFrame:
    return (df
            .withColumn("order_date", F.to_date("order_date"))
            .filter(F.col("order_id").isNotNull())
            .filter(F.col("customer_id").isNotNull() & (F.trim("customer_id") != ""))
            .filter(F.col("quantity") > 0)
            .filter(F.col("unit_price") > 0)
            .filter(F.col("order_date").isNotNull())
            .dropDuplicates(["order_id"])
            .withColumn("revenue", F.round(F.col("quantity") * F.col("unit_price"), 2)))


def run(spark: SparkSession, cfg: dict):
    bronze = spark.read.parquet(cfg["paths"]["bronze"])
    silver = clean(bronze)
    (silver.write.mode("overwrite")
           .partitionBy("order_date")          # partition pruning for date-range queries
           .parquet(cfg["paths"]["silver"]))
    return bronze.count(), silver.count()
