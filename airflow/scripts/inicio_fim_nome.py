def inicio_fim_nome(lista):
    if not lista:
        return ""
    return f"{lista[0]}_{lista[-1]}"