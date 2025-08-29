import os
import cdsapi
import logging
from datetime import datetime
from utils.variaveis import variaveis, ano, mes, dia, estatistica_diaria, tempo_UTC, frequencia, dataset

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
            "daily_statistic": estatistica_diaria,
            "time_zone": tempo_UTC,
            "frequency": frequencia,
            # "area": [90, -180, -90, 180] # [N, W, S, E] Comentando essa linha, obteremos os dados globais.
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
