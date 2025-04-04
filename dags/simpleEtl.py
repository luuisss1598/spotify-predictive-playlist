# airflow/dags/simple_etl_dag.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.core.connections.spotify_client import get_time
# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'simple_etl_pipeline',
    default_args=default_args,
    description='A simple ETL pipeline with print statements',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Define the extract function
def extract_data(**kwargs):
    print("Extracting data...")
    print("Data source: Spotify API")
    print("Extracting user listening history...")
    # Simulate data extraction
    data = {"timestamp": datetime.now().isoformat(), "status": "extracted"}
    print(f"Extracted data at {data['timestamp']}")
    print(get_time)
    return data

# Define the transform function
def transform_data(**kwargs):
    # Get the extracted data from the previous task
    ti = kwargs['ti']
    extracted_data = ti.xcom_pull(task_ids='extract_task')
    
    print("Transforming data...")
    print("Cleaning data...")
    print("Normalizing artist names...")
    print("Calculating listening frequencies...")
    
    # Simulate data transformation
    transformed_data = {
        "original_data": extracted_data,
        "timestamp": datetime.now().isoformat(),
        "status": "transformed"
    }
    
    print(f"Transformed data at {transformed_data['timestamp']}")
    return transformed_data

# Define the load function
def load_data(**kwargs):
    # Get the transformed data from the previous task
    ti = kwargs['ti']
    transformed_data = ti.xcom_pull(task_ids='transform_task')
    
    print("Loading data...")
    print("Target destination: Data Warehouse")
    print("Creating new tables if needed...")
    print("Inserting transformed data...")
    
    # Simulate data loading
    load_result = {
        "transformed_data": transformed_data,
        "timestamp": datetime.now().isoformat(),
        "records_loaded": 100,
        "status": "loaded"
    }
    
    print(f"Loaded {load_result['records_loaded']} records at {load_result['timestamp']}")
    return load_result

# Create the tasks
extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=extract_data,
    provide_context=True,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_task',
    python_callable=transform_data,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_task',
    python_callable=load_data,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
extract_task >> transform_task >> load_task