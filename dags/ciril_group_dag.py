from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.utils.edgemodifier import Label

default_args={
    'owner':'Simo',
    'retries':5,
    'retry_delay':timedelta(minutes=5)
}
"""
### Ciril Test DAG
"""
with DAG (
    dag_id='Ciril_group_test',
    default_args=default_args,
    start_date=datetime(2024,11,18),
    schedule=None,
    catchup=False
) as dag:
    
    create_ciril_db= BashOperator(
        task_id="create-db",
        bash_command="{{ '/opt/airflow/create-ciril-db.sh' | safe }}",
    )

    example_pandas = DockerOperator(
        task_id="run-example",
        image="airflow_ciril:latest",
        command=["python", "/opt/airflow/image-python/example.py"],
        docker_url="unix://var/run/docker.sock",
        api_version='auto',
        network_mode="cirilgroup",
        tty=True,
        entrypoint=None,
        working_dir="/opt/airflow/image-python",
    )

    load_data = DockerOperator(
        task_id="load_to_db",
        image="airflow_ciril:latest",
        command=["python", "/opt/airflow/load-csv/load_to_db.py"],
        docker_url="unix://var/run/docker.sock",
        api_version='auto',
        network_mode="cirilgroup",
        tty=True,
        entrypoint=None,
        working_dir="/opt/airflow/load-csv",
    )

    summarize_data = DockerOperator(
        task_id="summarize_data",
        image="airflow_ciril:latest",
        command=[
        "bash",
        "-c",
        "python /opt/airflow/summary-output/summary_output.py && cp /opt/airflow/data/summary_output.json ./data"],
        docker_url="unix://var/run/docker.sock",
        api_version='auto',
        network_mode="cirilgroup",
        mounts=[
            {
                "source": "/tmp/airflow/data",  
                "target": "/data",
                "type": "bind"
            }
        ],
        tty=True,
        entrypoint=None,
        working_dir="/opt/airflow/summary-output",
    )

    summarize_data.doc_md="""\
    # Title
    Test Restitution de données 
    """
    load_data.doc_md="""\
    # Test de chargement de données dans la BD MySQL
    """
    example_pandas.doc_md="""\
    # Restitution de données uniquement avec pandas
    """
    create_ciril_db.doc_md="""\
    # Script de création de la BD et des tables associé
    """
    [create_ciril_db,example_pandas] >> Label("Chargement de données") >> load_data >> Label("Restitution de données") >> summarize_data