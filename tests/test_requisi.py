#!/usr/bin/env python3
import os
import json
import subprocess

PARAMS = {
    "data_inicio": "1994-01-01",
    "data_fim": "2025-06-01",
    "dataset": [
        "reanalysis-era5-land",
        "reanalysis-era5-single-levels",
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
    'area': [-34.8, -73.9, 5.3, -34.8]
}

def run_request(dataset, variaveis, area):
    """Executa o main.py para um dataset e lista de variáveis."""
    cmd = [
        "python",
        "airflow/scripts/main.py",
        "--data_inicio", PARAMS["data_inicio"],
        "--data_fim", PARAMS["data_fim"],
        "--dataset", json.dumps(dataset),
        "--variaveis", json.dumps(variaveis),
        "--area", json.dumps(area),
    ]
    print("Comando:", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    if result.returncode != 0:
        print(f"❌ Erro na execução para dataset={dataset}")
    else:
        print(f"✅ Finalizado dataset={dataset}")

def main():

    run_request( PARAMS["dataset"], PARAMS["variaveis"], PARAMS["area"])

if __name__ == "__main__":
    main()



