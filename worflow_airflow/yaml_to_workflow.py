# -*- codingL utf-8 -*-
# @Time : 6/24/22 2:08 PM
# @Author : YIYANG BIAN
# @File : yaml_to_workflow.py

import yaml
import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Reading yaml file
script_path = os.path.dirname(os.path.realpath('/Users/bianyiyang/airflow/dags/CRUX/worflow_airflow/yaml_to_workflow.py'))
yaml_path = os.path.join(script_path, "peak_finding.yaml")

cfg = open(yaml_path, 'r').read()
yaml_info = yaml.load(cfg, Loader=yaml.FullLoader)

# default_args setting
default_args = {
    'owner': yaml_info['default_args']['owner'],
    'depends_on_past': yaml_info['default_args']['depends_on_past'],
    'start_date': eval(yaml_info['default_args']['start_date']),
    'email': yaml_info['default_args']['email'],
    'email_on_failure': yaml_info['default_args']['email_on_failure'],
    'email_on_retry': yaml_info['default_args']['email_on_retry'],
    'retries': yaml_info['default_args']['retries'],
    'retry_delay': eval(yaml_info['default_args']['retry_delay']),
}

# dag setting
dag = DAG(
    dag_id=yaml_info['dag']['name'],
    default_args=default_args,
    description="'" + yaml_info['dag']['description'] + "'",
    schedule_interval=yaml_info['dag']['schedule_interval'],
)

# task setting
task1 = BashOperator(
    task_id=yaml_info['tasks'][0]['task_id'],
    bash_command="cd /Users/bianyiyang/airflow/dags/CRUX/to_cards/ && python3 source.py --name 'Jacob L. Jones'\
                  --affiliation 'North Carolina State University'\
                  --positions 'Kobe Distinguished Professor, Materials Science and Engineering'\
                  --positions 'Director, Science and Technologies for Phosphorus Sustainability (STEPS) Center'\
                  --positions 'Director, Research Triangle Nanotechnology Network'\
                  --address '3072B Engineering Building I, Raleigh, NC'\
                  --phone 919-515-4557\
                  --email jacobjones@ncsu.edu && python3 source.py --name 'Mauro Sardela'\
                  --affiliation 'University of Illinois at Urbana-Champaign'\
                  --positions 'Director, Central Research Facilities, Materials Research Laboratory'\
                  --address '104 S. Goodwin Avenue – Urbana IL 61801'\
                  --website www.mrl.illinois.edu\
                  --phone 217-244-0547\
                  --email sardela@illinois.edu\
                  --office '#SC2014'",
    # python_callable=datacards,
    retries=yaml_info['tasks'][0]['retries'],
    dag=dag
)
