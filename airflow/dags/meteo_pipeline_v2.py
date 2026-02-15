from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Ajouter le chemin du projet pour pouvoir importer les modules src
sys.path.insert(0, '/opt/airflow')

from src.extract import WeatherExtractor
from src.transform import WeatherTransformer
from src.mongo_loader import MongoWeatherLoader

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def extract_task():
    """Tâche d'extraction des données météo"""
    extractor = WeatherExtractor()
    data = extractor.extract_all()
    extractor.save_raw(data)
    return f"✅ {len(data)} villes extraites"

def transform_task():
    """Tâche de transformation des données"""
    transformer = WeatherTransformer()
    data = transformer.load_latest_raw()
    df = transformer.transform_to_dataframe(data)
    df = transformer.engineer_features(df)
    path = transformer.save_processed(df)
    return f"✅ Données transformées: {path}"

def load_task():
    """Tâche de chargement dans MongoDB"""
    loader = MongoWeatherLoader(use_atlas=False)
    # À adapter selon ta fonction de chargement
    return "✅ Données chargées dans MongoDB"

with DAG(
    'meteo_maroc_pipeline_v2',
    default_args=default_args,
    description='Pipeline météo Maroc (version Python)',
    schedule_interval='0 6 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['meteo', 'maroc', 'python'],
) as dag:

    extract = PythonOperator(
        task_id='extract',
        python_callable=extract_task,
    )

    transform = PythonOperator(
        task_id='transform',
        python_callable=transform_task,
    )

    load = PythonOperator(
        task_id='load',
        python_callable=load_task,
    )

    extract >> transform >> load
