import pandas as pd

# Lê CSV
df1 = pd.read_csv("output_ultimo_valor_por_dia_total.csv")

# Remove primeira e última coluna extra
df1 = df1.iloc[:, 1:-1]

# Converte 'date' para datetime
df1['date'] = pd.to_datetime(df1['date'])

# Agrupa por dia e pega o último valor do dia
result = df1.groupby(df1['date'].dt.date).agg({
    'lon': 'first',        # mantém lon da primeira ocorrência do dia
    'lat': 'first',        # mantém lat da primeira ocorrência do dia
    'value': 'last'        # pega o último valor do dia
}).reset_index()

# Renomeia coluna do índice
result = result.rename(columns={'date': 'date'})

# Salva CSV final
result.to_csv("output_ultimo_valor_por_dia.csv", index=False)

