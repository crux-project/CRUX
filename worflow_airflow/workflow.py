# -*- codingL utf-8 -*-
# @Time : 5/12/22 6:18 PM
# @Author : YIYANG BIAN
# @File : worflow_airflow.py

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# from datacard import main as datacards

default_args = {
    'owner': 'byy',
    'depends_on_past': True,
    'start_date': datetime(2022, 6, 2),
    'email': ['byy981109@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='peak_finding',
    default_args=default_args,
    description='peakfinding',
    schedule_interval=timedelta(1)
)

task1 = BashOperator(
    task_id='source_information',
    bash_command="cd /Users/bianyiyang/airflow/dags/CRUX/to_cards/ && python3 generate_source.py --name 'Jacob L. Jones'\
                  --affiliation 'North Carolina State University'\
                  --positions 'Kobe Distinguished Professor, Materials Science and Engineering'\
                  --positions 'Director, Science and Technologies for Phosphorus Sustainability (STEPS) Center'\
                  --positions 'Director, Research Triangle Nanotechnology Network'\
                  --address '3072B Engineering Building I, Raleigh, NC'\
                  --phone 919-515-4557\
                  --email jacobjones@ncsu.edu && python3 generate_source.py --name 'Mauro Sardela'\
                  --affiliation 'University of Illinois at Urbana-Champaign'\
                  --positions 'Director, Central Research Facilities, Materials Research Laboratory'\
                  --address '104 S. Goodwin Avenue – Urbana IL 61801'\
                  --website www.mrl.illinois.edu\
                  --phone 217-244-0547\
                  --email sardela@illinois.edu\
                  --office '#SC2014'",
    # python_callable=datacards,
    retries=3,
    dag=dag
)


task2 = BashOperator(
    task_id='data_cards',
    bash_command="cd /Users/bianyiyang/airflow/dags/CRUX/to_cards/ && python3 datacard.py -file '../content/data/xrdml/NASA/BZnZr - BIn - BSc - PT/2.5Bi(Zn0.5Zr0.5)O3 - 5BiInO3 - 32.5BiScO3 - 60PbTiO3_1100C.xrdml'",
    # python_callable=datacards,
    retries=3,
    dag=dag
)

task3 = BashOperator(
    task_id='task_cards',
    bash_command="python3 /Users/bianyiyang/airflow/dags/CRUX/to_cards/taskcard.py peak_finding --input_format xrdml\
                                 --output_format txt\
                                 --input_parameters positions intensities\
                                 --output_parameters peaklist",
    # python_callable=x2,
    retries=3,
    dag=dag
)

task4 = BashOperator(
    task_id='model_cards',
    bash_command="cd /Users/bianyiyang/airflow/dags/CRUX/to_cards/ && python3 modelcard.py --modelName scipy.signal.find_peaks\
                     --affiliation 'The SciPy community'\
                     --contactInfo 'scipy-dev@python.org'\
                     --license 'BSD 3-Clause 'New' or 'Revised' License'\
                     --modelDate 02/05/2022\
                     --modelVersion 1.8.0\
                     --modelType 'Find peaks inside a signal based on peak properties.'\
                     --paperOrResource https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html\
                     --modelLocation https://github.com/scipy/scipy/blob/v1.8.0/scipy/signal/_peak_finding.py#L723-L1003\
                     --inputFormat nparray\
                     --outputFormat nparray\
                     --inputParameters x height threshold distance prominence width wlen rel_height plateau_size\
                     --outputParameters peaks properties && python3 modelcard.py --modelName peakutils.peak.index\
                     --username 'Lucas Hermann Negri'\
                     --contactInfo 'lucashnegri@gmail.com'\
                     --license 'MIT license'\
                     --modelDate 01/23/2020\
                     --modelVersion 1.3.3\
                     --modelType 'Peak detection routine.'\
                     --paperOrResource https://peakutils.readthedocs.io/en/latest/reference.html#module-peakutils.peak\
                     --modelLocation https://bitbucket.org/lucashnegri/peakutils\
                     --dependencies numpy scipy\
                     --inputFormat nparray\
                     --outputFormat nparray\
                     --inputParameters y thres min_dist thres_abs\
                     --outputParameters 'Array containing the numeric indexes of the peaks that were detected.'",
    # python_callable=x2,
    retries=3,
    dag=dag
)

task5 = BashOperator(
    task_id='scipy_model_cards',
    bash_command="cd /Users/bianyiyang/airflow/dags/CRUX/to_cards/ && python3 modelcard.py --modelName pf_scipy_dist200\
                     --modelLocation ../content/model/peakfinding/pf_scipy_dist200.py\
                     --dependencies scipy.signal.find_peaks\
                     --inputFormat xrdml\
                     --outputFormat txt\
                     --inputParameters positions intensities\
                     --outputParameters peaklist\
                     --hyperParameters min_dist=200\
                     --taskName peak_finding",
    retries=3,
    dag=dag
)


task6 = BashOperator(
    task_id='test_cards',
    bash_command="cd /Users/bianyiyang/airflow/dags/CRUX/to_cards/ && python3 testcard.py peak_finding",
    # python_callable=x2,
    retries=3,
    dag=dag
)

task7 = BashOperator(
    task_id='performance_cards',
    bash_command="python3 /Users/bianyiyang/airflow/dags/CRUX/to_cards/performance.py 0.01",
    retries=3,
    dag=dag
)

[task1, task2, task3] >> task4 >> task5 >> task6 >> task7
