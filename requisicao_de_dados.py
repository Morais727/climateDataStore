import os
import glob
import cdsapi
import logging
import subprocess
import pandas as pd
from datetime import datetime, timedelta
from utils.variaveis import variaveis, dataset 

logging.basicConfig(
    filename="requisicao.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

inicio = datetime.now()
logging.info("Início da requisição")

def concat_csv_por_ano(data_inicio, data_fim, variaveis):
    logging.info("Iniciando concatenação de CSVs por ano")
    if isinstance(data_inicio, str):
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
    if isinstance(data_fim, str):
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d")

    ano_de_inicio = data_inicio.year
    ano_de_fim = data_fim.year

    for ano in range(ano_de_inicio, ano_de_fim + 1):
        arquivos_csv = glob.glob(f"data/{variaveis[0]}/{ano}/csv/*.csv")
        if not arquivos_csv:
            logging.warning(f"Nenhum arquivo CSV encontrado para o ano {ano}")
            continue

        dfs = [pd.read_csv(arquivo) for arquivo in arquivos_csv]
        df_ano = pd.concat(dfs, ignore_index=True)
        df_ano['date'] = pd.to_datetime(df_ano['date'])
        df_ano = df_ano.sort_values('date').reset_index(drop=True)

        output_dir = f"data/{variaveis[0]}/{ano}"
        os.makedirs(output_dir, exist_ok=True)
        df_ano.to_csv(f"{output_dir}/all_data_{ano}.csv", index=False)
        logging.info(f"Concatenação de CSVs concluída para o ano {ano} ({len(df_ano)} registros)")

def inicio_fim_nome(lista):
    if not lista:
        return ""
    
    return f"{lista[0]}_{lista[-1]}"

def verifica_limite_fields(data_inicio, data_fim, lista_variaveis, limite=120000):
    # Converte strings para datetime
    if isinstance(data_inicio, str):
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
    if isinstance(data_fim, str):
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d")
    
    # Número de dias (delta)
    num_dias = (data_fim - data_inicio).days + 1  # +1 para incluir o último dia
    # Número de variáveis
    num_variaveis = len(lista_variaveis)
    
    # Calcula total de fields
    total_fields = num_variaveis * num_dias * 24  # 24 horas fixas

    # Verifica se ultrapassa limite
    ultrapassa = total_fields > limite
    
    return {
                'total_fields': total_fields,
                'ultrapassa_limite': ultrapassa
            }

def dividir_requisicao(data_inicio, data_fim, lista_variaveis, limite=120000):
    if isinstance(data_inicio, str):
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
    if isinstance(data_fim, str):
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d")
    
    resultado = verifica_limite_fields(data_inicio, data_fim, lista_variaveis, limite)
    total_fields = resultado['total_fields']
    ultrapassa = resultado['ultrapassa_limite']
    
    intervalos = []
    
    if ultrapassa:
        # Mantemos divisão por max_days_per_request
        max_days_per_request = limite // total_fields
        if max_days_per_request < 1:
            raise ValueError("Limite de fields muito baixo para o número de variáveis solicitado.")
        
        atual_inicio = data_inicio
        while atual_inicio <= data_fim:
            fim_ano = datetime(atual_inicio.year, 12, 31)
            atual_fim = min(atual_inicio + timedelta(days=max_days_per_request-1), fim_ano, data_fim)
            intervalos.append((atual_inicio, atual_fim))
            logging.info(f"Intervalo definido (ultrapassa limite): {atual_inicio.date()} -> {atual_fim.date()}")
            atual_inicio = atual_fim + timedelta(days=1)
    
    elif data_inicio.year != data_fim.year:
        # Se não ultrapassa, mas intervalos cruzam anos
        # Intervalo até fim do ano inicial
        fim_ano = datetime(data_inicio.year, 12, 31)
        intervalos.append((data_inicio, fim_ano))
        logging.info(f"Intervalo até fim do ano inicial: {data_inicio.date()} -> {fim_ano.date()}")
        
        # Intervalo do primeiro dia do ano seguinte até data_fim
        inicio_proximo_ano = datetime(data_fim.year, 1, 1)
        intervalos.append((inicio_proximo_ano, data_fim))
        logging.info(f"Intervalo ano seguinte: {inicio_proximo_ano.date()} -> {data_fim.date()}")
    
    else:
        # Se não ultrapassa e está dentro do mesmo ano
        intervalos.append((data_inicio, data_fim))
        logging.info(f"Intervalo dentro do mesmo ano e limite: {data_inicio.date()} -> {data_fim.date()}")
    
    return intervalos

def gera_anos(inicio, fim):
    return list(range(inicio, fim))

def gera_num(inicio, fim):
    return [f"{n:02}" for n in range(inicio, fim + 1)]

def gerar_horas(inicio, fim=None):
    if inicio == "dia":
        return [f"{h:02d}:00" for h in range(24)]
    
    if fim is None:
        raise ValueError("Para gerar intervalo, informe valor inicial e final")
    
    # Garante que os valores estejam no formato crescente
    if inicio <= fim:
        return [f"{h:02d}:00" for h in range(inicio, fim + 1)]
    else:
        return [f"{h:02d}:00" for h in range(inicio, fim - 1, -1)]

def faz_requisicao(variaveis, dia, mes, ano, horas, dataset=dataset):
    logging.info(f"Iniciando requisição: {dataset}, Variáveis: {variaveis}, Ano: {ano}, Mes: {mes[0]}-{mes[-1]}, Dias: {dia[0]}-{dia[-1]}, Horas: {horas[0]}-{horas[-1]}")
    
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
        "area": [-18, -52, -23, -47],
    }

    dias_nome = inicio_fim_nome(dia)
    mes_nome = inicio_fim_nome(mes)
    variaveis_nome = inicio_fim_nome(variaveis)
    variaveis_nome = variaveis_nome.replace("-", "_")

    output_hourly = f"{output_dir_base}/hourly"
    os.makedirs(output_hourly, exist_ok=True)

    nome_base = f'{dataset}_{variaveis_nome}_{ano}-{mes_nome}-{dias_nome}'
    target = f"{output_hourly}/{nome_base}.grib"

    logging.info(f"Baixando arquivo: {target}")
    client.retrieve(dataset, request).download(target)
    logging.info("Download concluído")

    output_celsius = f"{output_hourly}/{nome_base}_celsius.grib"
    resultado = subprocess.run(["cdo", "showname", f"{target}"], capture_output=True, text=True)
    variaveis_arq = resultado.stdout.splitlines()

    nova_var = f'{variaveis_arq[0]}_C'
    expr = f'{nova_var}={variaveis_arq[0]}-273.15'
    cmd_convert = f"cdo expr,'{expr}' {target} {output_celsius}"
    subprocess.run(cmd_convert, shell=True, check=True)
    logging.info(f"Conversão para Celsius concluída: {nova_var}")

    cmd_units = f"cdo -setattribute,{nova_var}@units=degC {output_celsius} {output_celsius}"
    subprocess.run(cmd_units, shell=True, check=True)

    output_daily = f'{output_dir_base}/daily_mean'
    os.makedirs(output_daily, exist_ok=True)
    cmd_daymean = f"cdo -daymean -shifttime,-1sec {output_celsius} {output_daily}/{nome_base}_daily.grib"
    subprocess.run(cmd_daymean, shell=True, check=True)
    logging.info("Cálculo daily mean concluído")

    output_csv = f'{output_dir_base}/csv'
    os.makedirs(output_csv, exist_ok=True)
    cmd_outputtab = f"cdo outputtab,date,lon,lat,value {output_daily}/{nome_base}_daily.grib | sed '2d' > {output_csv}/{nome_base}_daily.csv"
    subprocess.run(cmd_outputtab, shell=True, check=True)
    logging.info(f"Arquivo CSV gerado: {output_csv}/{nome_base}_daily.csv")

def main(data_inicio, data_fim):
    logging.info("Início do script")
    
    intervalos = dividir_requisicao(data_inicio, data_fim, variaveis)
    print(intervalos)
    for inicio, fim in intervalos:
        dia_inicio = inicio.day
        mes_inicio = inicio.month
        ano_inicio = inicio.year
        
        dia_fim = fim.day
        mes_fim = fim.month
        ano_fim = fim.year

        dia = gera_num(1, 31)
        mes = gera_num(mes_inicio, mes_fim)
        horas = gerar_horas("dia")
        ano = ano_inicio

        faz_requisicao(variaveis, dia, mes, ano, horas)

    concat_csv_por_ano(data_inicio, data_fim, variaveis)
    logging.info("Fim do script")

if __name__ == "__main__":
    data_inicio = "2024-01-01"
    data_fim = "2025-06-01"

    main(data_inicio, data_fim)
