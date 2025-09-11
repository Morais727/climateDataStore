import pandas as pd

# Caminho do CSV de entrada
input_csv = "maneira_burra/usa_cdo/total_precipitation/valparaiso/reanalysis_era5_land-total_precipitation-2024-01_12-01_31-milimetros-units.csv"
output_csv = "maneira_burra/usa_cdo/total_precipitation/valparaiso/media_mes/diff_por_dia.csv"

# Lê CSV
df = pd.read_csv(input_csv)

# Remove coluna inicial extra e última coluna se houver
df = df.iloc[:, 1:-1]

# Garante que a coluna 'date' seja datetime
df['date'] = pd.to_datetime(df['date'])

# Função para calcular diferença entre último e primeiro valor do dia
def first_last_diff(x):
    return x.iloc[-1] - x.iloc[0]

# Agrupa por dia e calcula
result = df.groupby(df['date'].dt.date).agg({
    'lon': 'first',       # mantém lon da primeira ocorrência
    'lat': 'first',       # mantém lat da primeira ocorrência
    'value': first_last_diff
})

# Transforma o índice (dia) em coluna
result.index.name = 'date'
result = result.reset_index()

# Salva CSV final
result.to_csv(output_csv, index=False)

print(f"CSV final salvo em: {output_csv}")


# import pandas as pd

# # Caminho do CSV de entrada
# input_csv = "output_ultimo_valor_por_dia_2025.csv"
# output_csv = "output_ultimo_valor_por_dia_total_mes_total.csv"

# # Lê CSV
# df = pd.read_csv(input_csv)

# # Remove primeira e última coluna extra se houver
# # df = df.iloc[:, 1:-1]

# # Garante que a coluna 'date' seja datetime
# df['date'] = pd.to_datetime(df['date'])

# # Cria coluna 'year_month' para agrupar por mês
# df['year_month'] = df['date'].dt.to_period('M')

# # Agrupa por mês e soma os valores
# monthly_sum = df.groupby('year_month').agg({
#     'value': 'sum',
#     'lon': 'first',   # mantém lon da primeira ocorrência do mês
#     'lat': 'first'    # mantém lat da primeira ocorrência do mês
# }).reset_index()

# # Converte 'year_month' de volta para string
# monthly_sum['year_month'] = monthly_sum['year_month'].astype(str)

# # Salva CSV final
# monthly_sum.to_csv(output_csv, index=False)

# print(f"CSV final com soma mensal salvo em: {output_csv}")
