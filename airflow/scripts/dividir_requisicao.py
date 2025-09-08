from datetime import datetime, timedelta
from limite_campos import verifica_limite_fields

def dividir_requisicao(data_inicio, data_fim, lista_variaveis, limite=120_000):
    if isinstance(data_inicio, str):
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
    if isinstance(data_fim, str):
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d")
    
    resultado = verifica_limite_fields(data_inicio, data_fim, lista_variaveis, limite)
    total_fields = resultado['total_fields']
    ultrapassa = resultado['ultrapassa_limite']
    
    intervalos = []
    
    if ultrapassa:
        max_days_per_request = limite // total_fields
        if max_days_per_request < 1:
            raise ValueError("Limite de fields muito baixo para o número de variáveis solicitado.")
        
        atual_inicio = data_inicio
        while atual_inicio <= data_fim:
            fim_ano = datetime(atual_inicio.year, 12, 31)
            atual_fim = min(atual_inicio + timedelta(days=max_days_per_request-1), fim_ano, data_fim)
            intervalos.append((atual_inicio, atual_fim))
            atual_inicio = atual_fim + timedelta(days=1)
    
    elif data_inicio.year != data_fim.year:
        fim_ano = datetime(data_inicio.year, 12, 31)
        intervalos.append((data_inicio, fim_ano))
        
        inicio_proximo_ano = datetime(data_fim.year, 1, 1)
        intervalos.append((inicio_proximo_ano, data_fim))
    
    else:
        intervalos.append((data_inicio, data_fim))
    
    return intervalos