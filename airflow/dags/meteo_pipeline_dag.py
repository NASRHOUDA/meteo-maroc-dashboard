from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'meteo_maroc_pipeline',
    default_args=default_args,
    description='Pipeline météo Maroc',
    schedule_interval='0 6 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['meteo', 'maroc'],
) as dag:

    extract = BashOperator(
        task_id='extract_data',
        bash_command='cd /opt/airflow && python -c "print(\"Extraction...\")"',
    )

    transform = BashOperator(
        task_id='transform_data',
        bash_command='cd /opt/airflow && python -c "print(\"Transformation...\")"',
    )

    load = BashOperator(
        task_id='load_data',
        bash_command='cd /opt/airflow && python -c "print(\"Chargement...\")"',
    )

    extract >> transform >> load
