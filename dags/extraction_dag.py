import sys

sys.path.insert(0, "/opt/airflow")

from datetime import datetime
import json

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from extraction.extraction import extraction


def extract_youtube(**context):
    data = extraction("@mim-repository")

    date_str = context["logical_date"].strftime("%Y-%m-%d")

    path = f"/opt/airflow/data/YT_data_{date_str}.json"

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Nombre de vidéos extraites : {len(data)}")
    print(f"JSON sauvegardé : {path}")

    return path


with DAG(
    dag_id="youtube_extraction",
    start_date=datetime(2026, 9, 16),
    schedule="@daily",
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id="extract_youtube",
        python_callable=extract_youtube,
    )

    trigger_warehouse = TriggerDagRunOperator(
        task_id="trigger_warehouse",
        trigger_dag_id="youtube_warehouse",
        wait_for_completion=False,
        conf={
            "json_path": "{{ ti.xcom_pull(task_ids='extract_youtube') }}"
        },
    )

    extract_task >> trigger_warehouse