import itertools
import json 
import argparse
from basicos import gera_num, gerar_horas
from faz_requisicao import faz_requisicao
from dividir_requisicao import dividir_requisicao

def main(data_inicio, data_fim, dataset, variaveis, area):
    intervalos = dividir_requisicao(data_inicio, data_fim, variaveis)

    arq_caminhos = []
    for inicio, fim in intervalos:
        mes_inicio = inicio.month
        ano_inicio = inicio.year
        mes_fim = fim.month
        
        dia = gera_num(1, 31)
        mes = gera_num(mes_inicio, mes_fim)
        horas = gerar_horas("dia")
        ano = ano_inicio

        # Produto cartesiano entre variáveis e datasets
        for var, ds in itertools.product(variaveis, dataset):
            arq_resultado = faz_requisicao(var, dia, mes, ano, horas, ds, area)
            arq_caminhos.append(arq_resultado)

    return arq_caminhos

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script para requisitar dados climáticos do ERA5.")

    parser.add_argument("--data_inicio", type=str, required=True, default="2024-01-01", help="Data de início da requisição (YYYY-MM-DD)")
    parser.add_argument("--data_fim", type=str, required=True, default="2024-01-01", help="Data de fim da requisição (YYYY-MM-DD)")
    parser.add_argument("--dataset", type=str, required=True, default="reanalysis-era5-land", help="Nome do dataset")
    parser.add_argument("--variaveis", type=str, required=True, default='["2m_temperature"]', help="Lista de variáveis em formato JSON")
    parser.add_argument("--area", type=str, required=False, default="None", help="Área geográfica em formato JSON")

    args = parser.parse_args()

    variaveis = json.loads(args.variaveis)
    area = json.loads(args.area)

    main(args.data_inicio, args.data_fim, args.dataset, variaveis, area)