from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator

with DAG(
    dag_id="exemplo_dag_gerenciamento_requisicoes_dados",
    schedule=None,  
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    tags=["exemplo", "dados"],
) as dag:
    
    # Task 1: Início do fluxo de trabalho
    start = EmptyOperator(
    task_id="inicio",
)

    # Task 2: Executa um script ou comando
    processar_dados = BashOperator(
        task_id="processar_dados",
        bash_command="echo 'Processando dados de vendas...' && sleep 5",
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
    start >> processar_dados >> carregar_dados >> fim



#  airflow api-server