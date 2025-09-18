import os
import cdsapi
from inicio_fim_nome import inicio_fim_nome

def faz_requisicao(var, dia, m, ano, horas, ds, area):    
    output_dir_base = f"data/{var}/{ano}/"
    os.makedirs(output_dir_base, exist_ok=True)

    client = cdsapi.Client()
    dataset = ds
    request = {
                    "variable": var,
                    "year": ano,
                    "month": m,
                    "day": dia,
                    "time": horas,
                    "data_format": "grib",
                    "download_format": "unarchived",
                    "area": area,
                }
    dias_nome = inicio_fim_nome(dia)
    variavel_nome = var.replace("-", "_")
    dataset_nome = dataset.replace("-", "_")
    output_hourly = f"{output_dir_base}/hourly"
    os.makedirs(output_hourly, exist_ok=True)

    nome_base = f'{dataset_nome}-{variavel_nome}-{ano}-{m}-{dias_nome}'
    target = f"{output_hourly}/{nome_base}.grib"
    print("\nRequest enviado:", request)
    
    client.retrieve(dataset, request).download(target)

    return target