def gera_anos(inicio, fim):
    return list(range(inicio, fim))

def gera_num(inicio, fim):
    return [f"{n:02}" for n in range(inicio, fim + 1)]

def gerar_horas(inicio, fim=None):
    if inicio == "dia":
        return [f"{h:02d}:00" for h in range(24)]
    
    if fim is None:
        raise ValueError("Para gerar intervalo, informe valor inicial e final")
    
    if inicio <= fim:
        return [f"{h:02d}:00" for h in range(inicio, fim + 1)]
    else:
        return [f"{h:02d}:00" for h in range(inicio, fim - 1, -1)]