import datetime

from airflow import utils 
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

yesterday = utils.dates.days_ago(1)

with DAG('using_XCOM_dag',schedule_interval='@daily',start_date=yesterday) as dag:

    def python_returning_value():
        """ This python function will return a value that will be automatically stored by Airflow using XCOm"""
        file_name = 'this_file_will_be_generated_by_another_python_function'
        return file_name
    
    def python_using_returned_value(**kargs):
        
        task_instance = kargs ['task_instance']
        file_name = task_instance.xcom_pull(task_ids = 'python_returning_value_task')
        
        with open('/home/airflow/gcs/data/{}'.format(file_name),'w') as f_obj:
            f_obj.write('File created using one function which got the file name from another function using XCOM')

    python_returning_value_op = PythonOperator(task_id='python_returning_value_task',python_callable=python_returning_value)
    python_using_returned_value_op = PythonOperator(task_id='python_using_returned_value_task',python_callable=python_using_returned_value,provide_context=True)

    python_returning_value_op >> python_using_returned_value_op
