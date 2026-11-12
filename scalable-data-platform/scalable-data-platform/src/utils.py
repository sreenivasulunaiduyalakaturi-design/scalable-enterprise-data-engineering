import logging
import yaml
from pyspark.sql import SparkSession


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    return logging.getLogger(name)


def load_config(path: str = "config/config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def get_spark(cfg: dict) -> SparkSession:
    return (SparkSession.builder
            .appName(cfg["app_name"])
            .master(cfg["spark"]["master"])
            .config("spark.sql.shuffle.partitions", cfg["spark"]["shuffle_partitions"])
            .config("spark.sql.adaptive.enabled", "true")   # adaptive query execution
            .getOrCreate())
