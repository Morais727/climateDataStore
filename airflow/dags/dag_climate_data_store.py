from __future__ import annotations
import os
import pendulum
from airflow.models.dag import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator

PARAMS = {
            "data_inicio": "1994-01-01",
            "data_fim": "2025-06-01",
            "dataset": '["reanalysis-era5-land","reanalysis-era5-single-levels"]',
            "variaveis": '["2m_temperature","total_precipitation"]',
            "area" : [-34.8, -73.9, 5.3, -34.8] # "area": "[-18, -52, -23, -47]"
        }

with DAG(
    dag_id="exemplo_dag_gerenciamento_requisicoes_dados",
    schedule=None,  
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    tags=["exemplo", "dados"],
) as dag:
    
    requisicao_dados = BashOperator(
        task_id="requisicao_dados",
        bash_command=(
                        f"python scripts/main.py "
                        f"--data_inicio {PARAMS['data_inicio']} "
                        f"--data_fim {PARAMS['data_fim']} "
                        f"--dataset {PARAMS['dataset']} "
                        f"--variaveis '{PARAMS['variaveis']}' "
                        f"--area '{PARAMS['area']}'"
                    ),
        cwd="/home/marcosmorais/airflow",  # Diretório de trabalho
        env={"PATH": "/home/marcosmorais/airflow_venv311/bin:" + os.environ["PATH"]},
                                    )
 
    converte_celsius = BashOperator(
        task_id="verifica_campos",
        bash_command="cmd showname ",
    )

    # Task 3: Simula o carregamento dos dados
    carregar_dados = BashOperator(
        task_id="carregar_dados",
        bash_command="echo 'Carregando dados para o banco de dados...'",
    )

    # Task 4: Fim do fluxo de trabalho
    fim = EmptyOperator(
        task_id="fim",
    )

    # Definindo a ordem das tasks
    requisicao_dados >> converte_celsius >> carregar_dados >> fim



# airflow api-server --host 0.0.0.0 --port 8080
# airflow standalone
# ssh -L 8080:localhost:8080 marcosmorais@177.105.35.229
# ~/airflow/logs/dag_id=exemplo_dag_gerenciamento_requisicoes_dados