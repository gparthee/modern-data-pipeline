from datetime import datetime,timezone
from airflow import DAG
from airflow.operators.bash import BashOperator
import os,shlex
project=shlex.quote(os.environ.get("DBT_PROJECT_DIR","/opt/airflow/portfolio"))
with DAG(dag_id="portfolio_revenue",start_date=datetime(2026,1,1,tzinfo=timezone.utc),schedule="@daily",catchup=False,max_active_runs=1) as dag:
    seed=BashOperator(task_id="seed",bash_command=f"cd {project} && dbt seed")
    build=BashOperator(task_id="build_and_test",bash_command=f"cd {project} && dbt build --exclude resource_type:seed")
    seed >> build
