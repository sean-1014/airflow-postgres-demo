from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator

dag_id = "postgres_demo_dag"

def transfer(source_conn_id, target_conn_id):
    from airflow.models import Variable
    import logging
    import psycopg
    import os

    source_password = Variable.get('source_db_password')
    target_password = Variable.get('target_db_password')
    
    source_conn = psycopg.connect(f'dbname=postgres user=postgres password={source_password} host=postgres-source')
    source_cursor = source_conn.cursor()
    target_conn = psycopg.connect(f'dbname=postgres user=postgres password={target_password} host=postgres-target')
    target_cursor = target_conn.cursor()

    try:
        target_cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales (
                  id SERIAL PRIMARY KEY,
                  creation_date DATE,
                  sale_value NUMERIC(10,2)
                );
            """)
        
        with source_cursor.copy("COPY sales TO STDOUT (FORMAT BINARY)") as src:
            with target_cursor.copy("COPY sales FROM STDIN (FORMAT BINARY)") as tgt:
                for data in src:
                    tgt.write(data)
        target_conn.commit()
        logging.info("Transferred data from source db to target db")
    except:
        logging.error('Could not copy table')
    finally:
        source_conn.close()
        source_cursor.close()
        target_conn.close()
        target_cursor.close()

with DAG(
    dag_id=dag_id,
    start_date=datetime(2022, 1, 1),
    schedule_interval="@once",
    catchup=False,
) as dag:
    transfer_data = PythonVirtualenvOperator(
        task_id='transfer_data',
        python_callable=transfer,
        requirements=['psycopg==3.0.15'],
        op_kwargs={
            'source_conn_id': 'source_db',
            'target_conn_id': "target_db"
        },
        dag=dag)
    
    transfer_data