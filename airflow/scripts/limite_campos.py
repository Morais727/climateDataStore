from datetime import datetime


def verifica_limite_fields(data_inicio, data_fim, lista_variaveis, limite=120_000):
    if isinstance(data_inicio, str):
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
    if isinstance(data_fim, str):
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d")
    
    num_dias = (data_fim - data_inicio).days + 1  # +1 para incluir o último dia
    num_variaveis = len(lista_variaveis)
    
    total_fields = num_variaveis * num_dias * 24  # 24 horas fixas

    ultrapassa = total_fields > limite
    
    return {
                'total_fields': total_fields,
                'ultrapassa_limite': ultrapassa
            }