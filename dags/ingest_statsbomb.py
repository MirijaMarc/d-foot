"""StatsBomb ingestion DAG. Placeholder: one no-op task until ingestion is written."""

from datetime import datetime

from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import DAG

with DAG(
    dag_id="ingest_statsbomb",
    schedule=None,  # manual trigger only for now
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["ingestion"],
):
    EmptyOperator(task_id="placeholder")
