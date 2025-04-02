from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from utils.test_function import get_data

default_args = {
    "owner": "Airflow",
    "depends_on_past": False,
    "email": "lherrera5034@gmail.com",
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2)  # Fixed typo here (removed the line break)
}

def get_data_test():
    return get_data()

with DAG(
    'ingest_test',
    default_args=default_args,
    description='Data pipeline to ingest data from Richmond data catalog, multiple endpoints.',
    schedule_interval=None,
    start_date=datetime(2025, 3, 24),
    catchup=False,
    tags=['water', 'api']
) as dag:
    # declare tasks to be used
    task_1 = EmptyOperator(
        task_id='task_1'
    )
    
    task_2 = EmptyOperator(
        task_id='task_2'
    )
    
    task_3 = PythonOperator(
        task_id='task_3',
        python_callable=get_data_test
    )
    
    task_1 >> task_2 >> task_3
