import os
import cdsapi
import zipfile
import logging
import rioxarray
import subprocess
import xarray as xr
from cdo import Cdo
import geopandas as gpd
from datetime import datetime
from utils.variaveis import variaveis, ano, mes, dia, horas, dataset  # estatistica_diaria, tempo_UTC, frequencia,

logging.basicConfig(
    filename="requisicao.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

inicio = datetime.now()
logging.info("Início da requisição")

client = cdsapi.Client()

dataset = dataset
request = {
    "variable": variaveis,
    "year": ano,
    "month": mes,
    "day": dia,
    "time": horas,
    # "daily_statistic": estatistica_diaria,
    # "time_zone": tempo_UTC,
    # "frequency": frequencia,
    "format": "netcdf",
    "download_format": "unarchived",
    "area": [6, -74.0, -33.7, -34.0],  # -> Brasil [N, W, S, E] Comentando essa linha, obteremos os dados globais.
}

if len(dia) > 10:
    dias_nome = dia[:10] + "_etc"

dias_nome = "_".join(dia)
mes_nome = "_".join(mes)

if len(variaveis) > 10:
    variaveis_nome = variaveis[:10] + "_etc"

variaveis_nome = "_".join(variaveis)

output_dir = f"data/{ano}/hourly"
os.makedirs(output_dir, exist_ok=True)

target = f"{output_dir}/{dataset}_{variaveis_nome}_{ano}-{mes_nome}-{dias_nome}.nc"

client.retrieve(dataset, request).download(target)

print(f"Arquivo salvo em: {target}")

fim = datetime.now()
duracao = fim - inicio

logging.info(f"Fim da requisição")
logging.info(f"Arquivo salvo em: {target}")
logging.info(f"Duração total: {duracao}")

logging.info("Início do processamento")

inicio = datetime.now()

ds = xr.open_dataset(target)

new_vars = {}

for var in ds.data_vars:
    da = ds[var]
    # Verifica se a variável tem atributo "units" = Kelvin
    if "units" in da.attrs and da.attrs["units"] in ["K", "kelvin", "Kelvin"]:
        print(f"✔ Convertendo {var} de Kelvin para Celsius")

        # Converte valores
        da_c = da - 273.15

        # Ajusta atributos
        da_c.attrs["units"] = "°C"
        da_c.name = var + "_C"

        new_vars[var + "_C"] = da_c
    else:
        # Mantém variável original
        new_vars[var] = da

# Cria novo dataset com variáveis convertidas
ds_new = xr.Dataset(new_vars, attrs=ds.attrs)

# Salva em NetCDF
output_nc = target.replace(".nc", "_celsius.nc")
ds_new.to_netcdf(output_nc)

output_daily = f"data/{ano}/daily_mean"
os.makedirs(output_daily, exist_ok=True)

cmd = f"cdo -daymean -shifttime,-1sec {output_nc} {output_daily}/{dataset}_{variaveis_nome}_{ano}-{mes_nome}-{dias_nome}_daily.nc"
subprocess.run(cmd, shell=True, check=True)

fim = datetime.now()
duracao = fim - inicio

logging.info(f"Fim do processamento")
logging.info(f"Duração total: {duracao}")
logging.info(f"Arquivo NetCDF salvo em: {output_nc}")

# === Ler shapefile do Brasil 2024 ===
brasil = gpd.read_file("/home/marcos-morais/Documentos/ZETTA/DOCS/BR_Pais_2024/BR_Pais_2024.shp")

# Reprojetar para WGS84 (ERA5 usa EPSG:4326)
brasil = brasil.to_crs("EPSG:4326")

# === Abrir dataset final (já convertido para Celsius) ===
ds_final = xr.open_dataset(output_nc)  # ou o arquivo diário, se preferir

# Escrever CRS no NetCDF (ERA5 é latitude/longitude)
ds_final = ds_final.rio.write_crs("EPSG:4326")

# === Recortar dados usando shapefile do Brasil ===
ds_brasil = ds_final.rio.clip(brasil.geometry, brasil.crs)

# === Salvar em novo arquivo NetCDF ===
output_br = output_nc.replace(".nc", "_brasil.nc")
ds_brasil.to_netcdf(output_br)

logging.info(f"Arquivo recortado para o Brasil salvo em: {output_br}")