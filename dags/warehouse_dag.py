import sys

sys.path.insert(0, "/opt/airflow")

from datetime import datetime
import os

from airflow import DAG
from airflow.operators.python import PythonOperator

from loading.postgres import staging_table_data
from loading.postgres import core_table_data


def load_staging(**context):

    date_str = context["logical_date"].strftime("%Y-%m-%d")

    default_path = f"/opt/airflow/data/YT_data_{date_str}.json"

    path = context["dag_run"].conf.get(
        "json_path",
        default_path
    )

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"JSON not found: {path}"
        )

    staging_table_data(path)

    print(f"JSON chargé dans Staging : {path}")


def load_core():

    core_table_data()

    print("Transformation + chargement Core terminés")


with DAG(
    dag_id="youtube_warehouse",
    start_date=datetime(2026, 9, 17),
    schedule=None,
    catchup=False,
) as dag:

    staging_task = PythonOperator(
        task_id="load_staging",
        python_callable=load_staging,
    )

    core_task = PythonOperator(
        task_id="load_core",
        python_callable=load_core,
    )

    staging_task >> core_task