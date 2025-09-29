import subprocess
import pandas as pd
import time
import logging
import os
import xarray as xr


# ========================
# CONFIGURAÇÕES
# ========================
input_file = "tests/comparacao/dados/teste_reanalysis_era5_land_jan_2024.grib"
output_dir = "tests/comparacao/dados/"
os.makedirs(output_dir, exist_ok=True)

log_file = os.path.join(output_dir, "comparacao.log")
logging.basicConfig(
    filename=log_file,
    filemode='w',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ========================
# MÉTODO 1 - CDO
# ========================
logging.info("=== Início processamento com CDO ===")
start_total = time.time()

# ------------------------
# 1. Processar temperatura 2t
# ------------------------
start = time.time()
output_2t = os.path.join(output_dir, "daily-2t_celsius.nc")
cmd_2t = f"cdo -subc,273.15 -daymean -selvar,2t {input_file} {output_2t}"
logging.info(f"Iniciando processamento da temperatura 2t:\n{cmd_2t}")
subprocess.run(cmd_2t, shell=True, check=True)
logging.info(f"Temperatura 2t processada. Arquivo de saída: {output_2t}. Tempo: {time.time() - start:.2f}s")

# ------------------------
# 2. Processar precipitação tp
# ------------------------
start = time.time()
output_tp = os.path.join(output_dir, "daily-tp_mm.nc")
cmd_tp = f"cdo -mulc,1000 -daysum -selvar,tp {input_file} {output_tp}"
logging.info(f"Iniciando processamento da precipitação tp:\n{cmd_tp}")
subprocess.run(cmd_tp, shell=True, check=True)
logging.info(f"Precipitação tp processada. Arquivo de saída: {output_tp}. Tempo: {time.time() - start:.2f}s")

# ------------------------
# 3. Exportar para CSV
# ------------------------
start = time.time()
csv_2t = os.path.join(output_dir, "saida_cdo_2t.csv")
cmd_csv_2t = f"cdo outputtab,date,lon,lat,value {output_2t} | tr -s ' ' ',' > {csv_2t}"
logging.info(f"Exportando temperatura 2t para CSV:\n{cmd_csv_2t}")
subprocess.run(cmd_csv_2t, shell=True, check=True)
logging.info(f"CSV de 2t gerado: {csv_2t}. Tempo: {time.time() - start:.2f}s")

start = time.time()
csv_tp = os.path.join(output_dir, "saida_cdo_tp.csv")
cmd_csv_tp = f"cdo outputtab,date,lon,lat,value {output_tp} | tr -s ' ' ',' > {csv_tp}"
logging.info(f"Exportando precipitação tp para CSV:\n{cmd_csv_tp}")
subprocess.run(cmd_csv_tp, shell=True, check=True)
logging.info(f"CSV de tp gerado: {csv_tp}. Tempo: {time.time() - start:.2f}s")

# ------------------------
# 4. Combinar CSVs
# ------------------------
start = time.time()

df_2t = pd.read_csv(csv_2t)
df_2t = df_2t.iloc[:, 1:-1]

df_tp = pd.read_csv(csv_tp)
df_tp = df_tp.iloc[:, 1:-1]

# Criar coluna 'day' a partir da data, se necessário
df_2t['day'] = pd.to_datetime(df_2t['date']).dt.date
df_tp['day'] = pd.to_datetime(df_tp['date']).dt.date

cols_join = ['day', 'lat', 'lon']
df_cdo = pd.merge(df_2t, df_tp, on=cols_join, suffixes=('_2t', '_tp'))
df_cdo = df_cdo[['day', 'lat', 'lon', 'value_2t', 'value_tp']]

csv_final_cdo = os.path.join(output_dir, "saida_cdo.csv")
df_cdo.to_csv(csv_final_cdo, index=False)
logging.info(f"CSV final combinado gerado: {csv_final_cdo}. Tempo: {time.time() - start:.2f}s")

end_total = time.time()
logging.info(f"=== Processamento CDO concluído. Tempo total: {end_total - start_total:.2f}s ===")

# ========================
# MÉTODO 2 - zarr
# ========================
logging.info("=== Início processamento com zarr ===")
start_zarr = time.time()

# ------------------------
# 1. Processar temperatura 2t
# ------------------------
ds = xr.open_dataset(input_file, engine="cfgrib")

# Selecionar variável 2t e calcular média diária
ds_2t = ds["t2m"].resample(time="1D").mean()
# Converter Kelvin para Celsius
ds_2t = ds_2t - 273.15

# Salvar em Zarr
zarr_2t = os.path.join(output_dir, "daily_2t_celsius")
ds_2t.to_dataset(name="2t").to_zarr(zarr_2t, mode="w")
logging.info(f"Temperatura 2t processada e salva em Zarr: {zarr_2t}. Tempo: {time.time()-start:.2f}s")

# ------------------------
# 2. Processar precipitação tp
# ------------------------
start = time.time()
# Selecionar variável tp e calcular soma diária
ds_tp = ds["tp"].resample(time="1D").sum()
# Converter m → mm
ds_tp = ds_tp * 1000

# Salvar em Zarr
zarr_tp = os.path.join(output_dir, "daily_tp_mm")
ds_tp.to_dataset(name="tp").to_zarr(zarr_tp, mode="w")
logging.info(f"Precipitação tp processada e salva em Zarr: {zarr_tp}. Tempo: {time.time()-start:.2f}s")

# # ------------------------
# # 3. Exportar para CSV
# # ------------------------
# start = time.time()

# # Função auxiliar para converter xarray → DataFrame com colunas date, lat, lon, value
# def xr_to_df(da, var_name):
#     df = da.to_dataframe().reset_index()
#     df = df.rename(columns={da.name: var_name, "time": "date"})
#     return df

# df_2t = xr_to_df(ds_2t, "2t")
# df_tp = xr_to_df(ds_tp, "tp")

# # Combinar dataframes por date, lat, lon
# cols_join = ['date', 'lat', 'lon']
# df_cdo = pd.merge(df_2t, df_tp, on=cols_join)

# # Salvar CSV final
# csv_final_cdo = os.path.join(output_dir, "saida_final.csv")
# df_cdo.to_csv(csv_final_cdo, index=False)
# logging.info(f"CSV final combinado gerado: {csv_final_cdo}. Tempo: {time.time()-start:.2f}s")

# end_total = time.time()
# logging.info(f"=== Processamento concluído. Tempo total: {end_total-start_zarr:.2f}s ===")

# Lista de arquivos intermediários
intermediarios = [
    # output_2t,  # daily-2t_celsius.nc
    # output_tp,  # tp_cdo.nc
    csv_2t,     # saida_cdo_2t.csv
    csv_tp      # saida_cdo_tp.csv
]

# Remover arquivos intermediários
for f in intermediarios:
    if os.path.exists(f):
        os.remove(f)
        logging.info(f"Arquivo intermediário removido: {f}")
        

# # ========================
# # MÉTODO 3 - xarray
# # ========================
# logging.info("=== Início processamento com xarray ===")
# start_xr = time.time()

# # 1. Abrir arquivo
# ds = xr.open_dataset(input_file)

# # 2. Média diária
# ds_daily = ds.resample(valid_time="1D").mean()

# # 3. Converter para Celsius apenas variáveis em Kelvin
# new_vars = {}
# for var in variaveis:
#     da = ds_daily[var]
#     if da.attrs.get("units", "K") in ["K", "kelvin", "Kelvin"]:
#         da_c = da - 273.15
#         da_c.attrs["units"] = "°C"
#         new_vars[var] = da_c
#     else:
#         new_vars[var] = da
# ds_celsius = xr.Dataset(new_vars, coords=ds_daily.coords)

# # 4. Exportar para CSV
# df_xr = ds_celsius.to_dataframe().reset_index()
# csv_final_xr = os.path.join(output_dir, "saida_xarray.csv")
# df_xr.to_csv(csv_final_xr, index=False)

# end_xr = time.time()
# logging.info(f"Tempo total xarray: {end_xr - start_xr:.2f} segundos")

