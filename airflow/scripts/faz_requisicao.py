import os
import cdsapi
from inicio_fim_nome import inicio_fim_nome

def faz_requisicao(variaveis, dia, mes, ano, horas, dataset, area):    
    output_dir_base = f"data/{variaveis[0]}/{ano}"
    os.makedirs(output_dir_base, exist_ok=True)

    client = cdsapi.Client()
    request = {
                    "variable": variaveis,
                    "year": ano,
                    "month": mes,
                    "day": dia,
                    "time": horas,
                    "data_format": "grib",
                    "download_format": "unarchived",
                    "area": area,
                }

    dias_nome = inicio_fim_nome(dia)
    mes_nome = inicio_fim_nome(mes)
    variaveis_nome = variaveis[0].replace("-", "_")
    dataset_nome = dataset.replace("-", "_")
    output_hourly = f"{output_dir_base}/hourly"
    os.makedirs(output_hourly, exist_ok=True)

    nome_base = f'{dataset_nome}-{variaveis_nome}-{ano}-{mes_nome}-{dias_nome}'
    target = f"{output_hourly}/{nome_base}.grib"

    client.retrieve(dataset, request).download(target)