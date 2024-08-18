from airflow import DAG
from airflow.utils.dates import days_ago
from operators.greenplum import GreenplumOperator

default_args = {
    'owner': 'airflow',
    'retries': 1,
}

with DAG(
    dag_id='example_greenplum_dag',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
) as dag:

    run_sql_task = GreenplumOperator(
        task_id='run_sql_task',
        sql='CREATE TABLE landing.DUMMY AS SELECT * FROM pg_catalog.pg_tables LIMIT 10;',
        gp_conn_id='gp_conn_id',
    )

run_sql_task