import pandas as pd

# Caminho dos CSVs
csv1 = "maneira_burra/usa_cdo/total_precipitation/valparaiso/reanalysis_era5_land-total_precipitation-2024-01_12-01_31-milimetros-units-daymax.csv"
csv2 = "maneira_burra/usa_cdo/total_precipitation/valparaiso/reanalysis_era5_land-total_precipitation-2024-01_12-01_31-milimetros-units-daymin.csv"
output_csv = "maneira_burra/usa_cdo/total_precipitation/valparaiso/media_mes/diferenca_diaria.csv"

# Lê os CSVs
df1 = pd.read_csv(csv1)
df2 = pd.read_csv(csv2)

# Remove primeira e última coluna se forem extras (como no seu caso)
df1 = df1.iloc[:, 1:-1]
df2 = df2.iloc[:, 1:-1]

# Converte a coluna 'date' para datetime
df1['date'] = pd.to_datetime(df1['date'])
df2['date'] = pd.to_datetime(df2['date'])

# Pega apenas o primeiro valor do dia em cada CSV
df1_day = df1.groupby(df1['date'].dt.date)['value'].first().reset_index()
df2_day = df2.groupby(df2['date'].dt.date)['value'].first().reset_index()

# Renomeia as colunas para identificar
df1_day = df1_day.rename(columns={'value': 'value1'})
df2_day = df2_day.rename(columns={'value': 'value2'})

# Junta os dois DataFrames pelo dia
merged = pd.merge(df1_day, df2_day, on='date', how='inner')

# Calcula a diferença entre os valores de cada dia
merged['diff'] = merged['value1'] - merged['value2']

# Salva o CSV final
merged.to_csv(output_csv, index=False)
