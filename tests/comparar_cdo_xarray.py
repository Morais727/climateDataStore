import subprocess
import xarray as xr
import pandas as pd
import time
import logging
import os

# ========================
# CONFIGURAÇÕES
# ========================
input_file = "data/2025/hourly/reanalysis-era5-land_2m_dewpoint_temperature_skin_temperature_2025-01-01_02_03_04_05_06_07_08_09_10.nc"
output_dir = "comparacao"
os.makedirs(output_dir, exist_ok=True)

log_file = os.path.join(output_dir, "comparacao.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

variaveis = ["d2m", "skt"]

# ========================
# MÉTODO 1 - CDO
# ========================
logging.info("=== Início processamento com CDO ===")
start_cdo = time.time()

# 1. Média diária + shift time
daily_file = os.path.join(output_dir, "daily_cdo.nc")
cmd_daymean = f"cdo -daymean -shifttime,-1sec {input_file} {daily_file}"
subprocess.run(cmd_daymean, shell=True, check=True)

# 2. Converter de Kelvin para Celsius (para ambas as variáveis)
celsius_file = os.path.join(output_dir, "daily_cdo_celsius.nc")
cmd_celsius = f"cdo subc,273.15 {daily_file} {celsius_file}"
subprocess.run(cmd_celsius, shell=True, check=True)

# 3. Exportar para CSV (uma variável de cada vez e depois juntar no pandas)
dfs = []
for var in variaveis:
    csv_file = os.path.join(output_dir, f"{var}_cdo.csv")
    cmd_csv = f"cdo outputtab,date,lat,lon,value -selvar,{var} {celsius_file} > {csv_file}"
    subprocess.run(cmd_csv, shell=True, check=True)
    df = pd.read_csv(
                        csv_file,
                        sep=r"\s+",
                        comment="#",          # ignora linhas começando com "#"
                        skip_blank_lines=True,
                        names=["date", "lat", "lon", var],
                        dtype={var: float},
                        engine="python"
                    )

    dfs.append(df)

# Juntar variáveis em único CSV
for i in range(len(dfs)):
    dfs[i]["date"] = dfs[i]["date"].astype(str)
    dfs[i]["lat"]  = dfs[i]["lat"].astype(float)
    dfs[i]["lon"]  = dfs[i]["lon"].astype(float)

df_final_cdo = pd.merge(dfs[0], dfs[1], on=["date", "lat", "lon"], how="inner")
csv_final_cdo = os.path.join(output_dir, "saida_cdo.csv")
df_final_cdo.to_csv(csv_final_cdo, index=False)

end_cdo = time.time()
logging.info(f"Tempo total CDO: {end_cdo - start_cdo:.2f} segundos")

# ========================
# MÉTODO 2 - xarray
# ========================
logging.info("=== Início processamento com xarray ===")
start_xr = time.time()

# 1. Abrir arquivo
ds = xr.open_dataset(input_file)

# 2. Média diária
ds_daily = ds.resample(valid_time="1D").mean()

# 3. Converter para Celsius apenas variáveis em Kelvin
new_vars = {}
for var in variaveis:
    da = ds_daily[var]
    if da.attrs.get("units", "K") in ["K", "kelvin", "Kelvin"]:
        da_c = da - 273.15
        da_c.attrs["units"] = "°C"
        new_vars[var] = da_c
    else:
        new_vars[var] = da
ds_celsius = xr.Dataset(new_vars, coords=ds_daily.coords)

# 4. Exportar para CSV
df_xr = ds_celsius.to_dataframe().reset_index()
csv_final_xr = os.path.join(output_dir, "saida_xarray.csv")
df_xr.to_csv(csv_final_xr, index=False)

end_xr = time.time()
logging.info(f"Tempo total xarray: {end_xr - start_xr:.2f} segundos")

logging.info("=== Processamento concluído ===")

print(f"Resultados salvos em: {output_dir}")
print(f"- CSV via CDO: {csv_final_cdo}")
print(f"- CSV via xarray: {csv_final_xr}")
print(f"Veja os tempos no log: {log_file}")
