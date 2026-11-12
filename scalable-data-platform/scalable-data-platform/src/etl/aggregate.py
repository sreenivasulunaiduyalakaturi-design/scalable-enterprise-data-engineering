"""Gold layer: business-ready aggregates for BI / ML consumers."""
from pyspark.sql import DataFrame, SparkSession, functions as F


def daily_category_revenue(silver: DataFrame) -> DataFrame:
    return (silver.groupBy("order_date", "category")
            .agg(F.sum("revenue").alias("total_revenue"),
                 F.countDistinct("order_id").alias("orders"))
            .orderBy("order_date", "category"))


def top_customers(silver: DataFrame, n: int = 20) -> DataFrame:
    return (silver.groupBy("customer_id")
            .agg(F.sum("revenue").alias("lifetime_value"), F.count("*").alias("orders"))
            .orderBy(F.desc("lifetime_value")).limit(n))


def run(spark: SparkSession, cfg: dict):
    silver = spark.read.parquet(cfg["paths"]["silver"])
    daily_category_revenue(silver).write.mode("overwrite").parquet(f'{cfg["paths"]["gold"]}/daily_revenue')
    top_customers(silver).write.mode("overwrite").parquet(f'{cfg["paths"]["gold"]}/top_customers')
