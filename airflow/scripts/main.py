from dividir_requisicao import dividir_requisicao
from basicos import gera_num, gerar_horas
from faz_requisicao import faz_requisicao

def main(data_inicio, data_fim, dataset, variaveis, area):
    intervalos = dividir_requisicao(data_inicio, data_fim, variaveis)
    for inicio, fim in intervalos:
        mes_inicio = inicio.month
        ano_inicio = inicio.year
        
        mes_fim = fim.month

        dia = gera_num(1, 31)
        mes = gera_num(mes_inicio, mes_fim)
        horas = gerar_horas("dia")
        ano = ano_inicio

        faz_requisicao(variaveis, dia, mes, ano, horas, dataset, area)

if __name__ == "__main__":
    data_inicio = "2024-01-01"
    data_fim = "2025-06-01"

    dataset = "reanalysis-era5-land" 
    variaveis = ["2m_temperature"]
    area = [-18, -52, -23, -47]

    main(data_inicio, data_fim, dataset, variaveis, area)
