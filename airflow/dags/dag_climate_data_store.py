from __future__ import annotations
import os
import json
import pendulum
from airflow.models.dag import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator


PARAMS = {
    "data_inicio": "1994-01-01",
    "data_fim": "2025-06-01",
    "dataset": [
                    "reanalysis-era5-single-levels",
                    "reanalysis-era5-land",                     
                ],
    "variaveis": [
                    "2m_dewpoint_temperature",
                    "2m_temperature",
                    "skin_temperature",
                    "soil_temperature_level_1",
                    "soil_temperature_level_2",
                    "soil_temperature_level_3",
                    "soil_temperature_level_4",
                    "skin_reservoir_content",
                    "volumetric_soil_water_layer_1",
                    "volumetric_soil_water_layer_2",
                    "volumetric_soil_water_layer_3",
                    "volumetric_soil_water_layer_4",
                    "forecast_albedo",
                    "surface_latent_heat_flux",
                    "surface_net_solar_radiation",
                    "surface_net_thermal_radiation",
                    "surface_sensible_heat_flux",
                    "surface_solar_radiation_downwards",
                    "surface_thermal_radiation_downwards",
                    "10m_u_component_of_wind",
                    "10m_v_component_of_wind",
                    "surface_pressure",
                    "total_precipitation",
                ],
    "area": [-34.8, -73.9, 5.3, -34.8],
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
            "python scripts/main.py "
            f"--data_inicio {PARAMS['data_inicio']} "
            f"--data_fim {PARAMS['data_fim']} "
            f"--dataset '{json.dumps(PARAMS['dataset'])}' "
            f"--variaveis '{json.dumps(PARAMS['variaveis'])}' "
            f"--area '{json.dumps(PARAMS['area'])}' "
        ),
        cwd="/home/marcosmorais/airflow",  # Diretório de trabalho
        env={"PATH": "/home/marcosmorais/airflow_venv311/bin:" + os.environ["PATH"]},
    )

    requisicao_dados
