"""Airflow DAG: orchestrates the three stages daily."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {"retries": 2, "retry_delay": timedelta(minutes=5)}

with DAG("sales_pipeline", start_date=datetime(2024, 1, 1), schedule="@daily",
         catchup=False, default_args=default_args) as dag:
    ingest = BashOperator(task_id="ingest", bash_command="cd /opt/project && python -m src.main --stage ingest")
    transform = BashOperator(task_id="transform", bash_command="cd /opt/project && python -m src.main --stage transform")
    aggregate = BashOperator(task_id="aggregate", bash_command="cd /opt/project && python -m src.main --stage aggregate")
    ingest >> transform >> aggregate
