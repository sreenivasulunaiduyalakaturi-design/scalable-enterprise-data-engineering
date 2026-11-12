# Scalable Enterprise Data Engineering – Base Project

A medallion-architecture (Bronze → Silver → Gold) batch pipeline built on **Apache Spark**.

```
raw CSV ──ingest──► Bronze (parquet) ──clean + DQ gate──► Silver (partitioned parquet) ──aggregate──► Gold (BI tables)
```

## Quick start (needs Python 3.9+ and Java 11/17)
```bash
make install
make data      # generate sample sales data
make run       # run full pipeline
make test
```
Outputs land in `data/bronze`, `data/silver`, `data/gold`.

## Why it scales
- Spark distributes work; change `spark.master` to YARN / Kubernetes / Databricks with no code changes.
- Columnar Parquet + `partitionBy(order_date)` enables partition pruning.
- Adaptive query execution and tunable shuffle partitions in `config.yaml`.
- Config-driven paths; stages independently runnable (`--stage ingest|transform|aggregate`).
- Data-quality gate stops bad loads; Airflow DAG (`dags/`) handles scheduling and retries.

## Ideas to extend
Delta Lake/Iceberg tables, Kafka streaming ingestion, dbt models, Great Expectations, CI/CD, cloud storage (S3/ADLS).
