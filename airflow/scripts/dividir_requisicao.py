import logging
from datetime import datetime, timedelta
from limite_campos import verifica_limite_fields

logging.basicConfig(level=logging.INFO)

def dividir_requisicao(data_inicio, data_fim, limite=120_000):
    if isinstance(data_inicio, str):
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
    if isinstance(data_fim, str):
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d")
    
    resultado = verifica_limite_fields(data_inicio, data_fim, limite)
    total_fields = resultado['total_fields']
    ultrapassa = resultado['ultrapassa_limite']
    
    intervalos = []
    
    if ultrapassa:
        num_dias = (data_fim - data_inicio).days + 1
        fields_por_dia = max(total_fields // num_dias, 1)
        max_days_per_request = max(limite // fields_por_dia, 1)  # garante pelo menos 1 dia
        
        atual_inicio = data_inicio
        while atual_inicio <= data_fim:
            fim_ano = datetime(atual_inicio.year, 12, 31)
            atual_fim = min(atual_inicio + timedelta(days=max_days_per_request-1), fim_ano, data_fim)
            intervalos.append((atual_inicio, atual_fim))
            logging.info(f"Intervalo definido (ultrapassa limite): {atual_inicio.date()} -> {atual_fim.date()}")
            atual_inicio = atual_fim + timedelta(days=1)
    
    elif data_inicio.year != data_fim.year:
        fim_ano = datetime(data_inicio.year, 12, 31)
        intervalos.append((data_inicio, fim_ano))
        logging.info(f"Intervalo até fim do ano inicial: {data_inicio.date()} -> {fim_ano.date()}")
        
        inicio_proximo_ano = datetime(data_fim.year, 1, 1)
        intervalos.append((inicio_proximo_ano, data_fim))
        logging.info(f"Intervalo ano seguinte: {inicio_proximo_ano.date()} -> {data_fim.date()}")
    
    else:
        intervalos.append((data_inicio, data_fim))
        logging.info(f"Intervalo dentro do mesmo ano e limite: {data_inicio.date()} -> {data_fim.date()}")
    
    return intervalos
