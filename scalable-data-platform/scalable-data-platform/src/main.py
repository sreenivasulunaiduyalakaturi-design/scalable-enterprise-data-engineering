"""Pipeline entry point:  python -m src.main --stage all"""
import argparse
from src.utils import get_spark, load_config, get_logger
from src.etl import ingest, transform, aggregate, quality

log = get_logger("pipeline")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--stage", choices=["ingest", "transform", "aggregate", "all"], default="all")
    p.add_argument("--config", default="config/config.yaml")
    args = p.parse_args()

    cfg = load_config(args.config)
    spark = get_spark(cfg)
    try:
        if args.stage in ("ingest", "all"):
            log.info("Bronze rows: %s", ingest.run(spark, cfg))
        if args.stage in ("transform", "all"):
            b, s = transform.run(spark, cfg)
            ratio = quality.check_bad_row_ratio(b, s, cfg["quality"]["max_bad_row_ratio"])
            log.info("Silver rows: %s (rejected %.2f%%)", s, ratio * 100)
        if args.stage in ("aggregate", "all"):
            aggregate.run(spark, cfg)
            log.info("Gold tables written")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
