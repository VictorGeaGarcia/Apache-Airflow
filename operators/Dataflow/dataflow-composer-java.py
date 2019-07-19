from airflow import models
from airflow.operators import python_operator
from airflow.contrib.operators.dataflow_operator import DataFlowJavaOperator
 
from google.cloud import bigquery
import datetime
 
yesterday = datetime.datetime.combine(
    datetime.datetime.today()-datetime.timedelta(1),
    datetime.datetime.min.time()
)
 
default_dag_args = {'start_date':yesterday}
 
with models.DAG(
        'composer-dataflow-java',
        schedule_interval = datetime.timedelta(days=1),
        default_args=default_dag_args) as dag:

    dataflow_java_task = DataFlowJavaOperator(jar='/home/airflow/gcs/data/google-cloud-teleport-java-0.1-SNAPSHOT.jar',
        task_id='start-pipeline',
        options={
            'project':'<PROJECT_ID>',
            'tempLocation':'<GCS_BUCKET>',
            'inputTopic':'<INPUT_TOPIC>',
            'outputTableSpec':'<output_table>'})

    dataflow_java_task
