XCOM is the Airflow way to exchange data between tasks. You can either call it explicitely (by calling "xcom_push()")
or implicitely anything returned from PythonOperator goes here.
Official docs https://airflow.apache.org/concepts.html#xcoms Explanation from SO post: https://stackoverflow.com/questions/50149085/python-airflow-return-result-from-pythonoperator

My file pythonoperator-xcom.py contains two tasks:
task python_returning_value_task will run the python function python_returning_value which simply returns a string.

task python_using_returned_value_task will run the python function python_using_returned_value using the value returned by the previous task. To access this value you need to add **whatever to your python function:

def python_using_returned_value(**kargs):

and later on access the task_instance key doing:

task_instance = kargs ['task_instance'] file_name = task_instance.xcom_pull(task_ids = 'python_returning_value_task')
