# -*- codingL utf-8 -*-
# @Time : 5/12/22 6:18 PM
# @Author : YIYANG BIAN
# @File : workflow.py

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# from datacard import main as datacards

default_args = {
    'owner': 'byy',
    'depends_on_past': True,
    'start_date': datetime(2022, 5, 12),
    'email': ['byy981109@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'peak_finding',
    default_args=default_args,
    description='peakfinding',
    schedule_interval=timedelta(1)
)

task1 = BashOperator(
    task_id='data_cards',
    bash_command="cd /Users/bianyiyang/airflow/dags/CRUX/to_cards & python3 datacard.py",
    # python_callable=datacards,
    retries=3,
    dag=dag
)

task2 = BashOperator(
    task_id='task_cards',
    bash_command="/Users/bianyiyang/airflow/dags/CRUX/to_cards/task_cards.sh ",
    # python_callable=x2,
    retries=3,
    dag=dag
)

task3 = BashOperator(
    task_id='model_cards',
    bash_command="/Users/bianyiyang/airflow/dags/CRUX/to_cards/model_cards.sh ",
    # python_callable=x2,
    retries=3,
    dag=dag
)

task4 = BashOperator(
    task_id='test_cards',
    bash_command="/Users/bianyiyang/airflow/dags/CRUX/to_cards/test_card.sh ",
    # python_callable=x2,
    retries=3,
    dag=dag
)

task5 = BashOperator(
    task_id='performance_cards',
    bash_command="/Users/bianyiyang/airflow/dags/CRUX/to_cards/performance.sh ",
    retries=3,
    dag=dag
)

task1
task2
task3
task4 >> task5

