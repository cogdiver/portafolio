

# """ETL workflow"""

# Airflow dependencies
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.dummy import DummyOperator


from datetime import datetime


default_args = {
    "owner": "Airflow",
    "start_date": days_ago(2),
}

# funciones
def func_1(**context):
    print('func_1')
    # print(context)
    context["task_instance"].xcom_push(key="model_id", value='model_id_1')

    return [f'task_{i}' for i in [2,3]]


def func_5(**context):
    model_id = context["task_instance"].xcom_pull(task_ids="task_1", key="model_id")
    print('*'*20)
    print(model_id)
    print('*'*20)


def func_6(templates_dict, **context):
    print('*'*20)
    print(templates_dict['model_id'])
    print('*'*20)


with DAG(
    dag_id="example",
    catchup=False,
    schedule_interval="0 0 * * *",
    default_args=default_args,
) as dag:

    task1 = BranchPythonOperator(
        task_id = "task_1",
        python_callable = func_1,
    )

    task2 = DummyOperator(
        task_id = "task_2"
    )

    task3 = DummyOperator(
        task_id = "task_3"
    )

    task4 = DummyOperator(
        task_id = "task_4"
    )

    task5 = PythonOperator(
        task_id = "task_5",
        python_callable = func_5,
        trigger_rule = 'none_failed_min_one_success'
    )

    task6 = PythonOperator(
        task_id = "task_6",
        python_callable = func_6,
        templates_dict={
            "model_id": "{{task_instance.xcom_pull(task_ids='task_1', key='model_id')}}"
        },
        trigger_rule = 'none_failed_min_one_success'
    )

    # dependencies
    task1 >> [task2, task3, task4] >> task5 >> task6
