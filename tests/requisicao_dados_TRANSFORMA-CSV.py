import os
import cdsapi
import zipfile
import logging
import xarray as xr
from cdo import Cdo
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
    "area": [-19, -48, -23, -43] # [N, W, S, E] Comentando essa linha, obteremos os dados globais.
}
dias_nome = "_".join(dia)
mes_nome = "_".join(mes)

if len(variaveis) > 10:
    variaveis_nome = variaveis[:10] + "_etc"

variaveis_nome = "_".join(variaveis)

output_dir = f"data/{ano}"
os.makedirs(output_dir, exist_ok=True)

target = f"{output_dir}/{dataset}_{variaveis_nome}_{ano}-{mes_nome}-{dias_nome}.nc"

client.retrieve(dataset, request).download(target)

print(f"Arquivo salvo em: {target}")

fim = datetime.now()
duracao = fim - inicio

logging.info(f"Fim da requisição")
logging.info(f"Arquivo salvo em: {target}")
logging.info(f"Duração total: {duracao}")

logging.info("Início do processamento com CDO")

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

# Converte para CSV (tratando casos com e sem dimensões)
output_csv = output_nc.replace(".nc", ".csv")

        
df = ds_new.to_dataframe().reset_index()
df.to_csv(output_csv, index=False)

fim = datetime.now()
duracao = fim - inicio

logging.info(f"Fim do processamento")
logging.info(f"Duração total: {duracao}")
logging.info(f"Arquivo NetCDF salvo em: {output_nc}")
logging.info(f"Arquivo CSV salvo em: {output_csv}")
