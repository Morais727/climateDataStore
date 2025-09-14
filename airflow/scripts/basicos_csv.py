import os
import glob
import pandas as pd
from datetime import datetime

def corrig_csv(arquino, colunas):
    df = pd.read_csv(arquino)
    df = df.drop(columns=colunas, errors='ignore')
    df.to_csv(arquino, index=False)  
    return df

def concat_csv_por_ano(data_inicio, data_fim, variaveis):
    if isinstance(data_inicio, str):
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
    if isinstance(data_fim, str):
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d")

    ano_de_inicio = data_inicio.year
    ano_de_fim = data_fim.year

    for ano in range(ano_de_inicio, ano_de_fim + 1):
        arquivos_csv = glob.glob(f"data/{variaveis}/{ano}/csv/*.csv")
        if not arquivos_csv:
            continue

        dfs = [pd.read_csv(arquivo) for arquivo in arquivos_csv]
        df_ano = pd.concat(dfs, ignore_index=True)
        df_ano['date'] = pd.to_datetime(df_ano['date'])
        df_ano = df_ano.sort_values('date').reset_index(drop=True)

        output_dir = f"data/{variaveis}/{ano}"
        os.makedirs(output_dir, exist_ok=True)
        df_ano.to_csv(f"{output_dir}/all_data_{ano}.csv", index=False)

        arq_entrada = f"{output_dir}/all_data_{ano}.csv"
        colunas = ['#', 'Unnamed: 5']
        corrig_csv(arq_entrada, colunas)
