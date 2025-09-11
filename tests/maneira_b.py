# import os
# import glob
# import pandas as pd
# import subprocess

# files_to_process = [
#     "ERA5_SINGLE/2024/reanalysis_era5_single_levels-total_precipitation-2024-01_12-01_31-milimetros-units.grib",
#     "ERA5_SINGLE/2025/reanalysis_era5_single_levels-total_precipitation-2025-01_06-01_31-milimetros-units.grib"
# ] 

# destination_dir = 'ERA5_SINGLE/tratados'
# os.makedirs(destination_dir, exist_ok=True)

# for file_path in files_to_process:
#     filename = os.path.basename(file_path)
    
#     # --- Passo 1: calcular média mensal ---
#     monmean_file = os.path.join(destination_dir, f"monsum_{filename}")
#     command = f"cdo -monsum {file_path} {monmean_file}"
#     subprocess.run(command, shell=True)
    
#     # --- Passo 2: gerar CSV com outputtab ---
#     csv_file = os.path.join(destination_dir, filename.replace('.grib', '.csv'))
#     command = f"cdo -outputtab,date,lon,lat,value -remapnn,lon=-50.900466_lat=-21.164700 {monmean_file} | tr -s ' ' ',' > {csv_file}"
#     subprocess.run(command, shell=True)
    
#     # --- Passo 3: limpar CSV (remover segunda linha e primeira/última coluna) ---
#     # Lê CSV ignorando a segunda linha (índice 1)
#     df = pd.read_csv(csv_file, skiprows=[1])
    
#     # Remove primeira e última coluna
#     df = df.iloc[:, 1:-1]
    
#     # Salva CSV final
#     df.to_csv(csv_file, index=False)
    
#     print(f"Processado e salvo: {csv_file}")



import os
import pandas as pd
import subprocess

files_to_process = [
    "data/ERA5_SINGLE/2024/reanalysis_era5_single_levels-2m_temperature-2024-01_12-01_31-celsius-units.grib",
    "data/ERA5_SINGLE/2025/reanalysis_era5_single_levels-2m_temperature-2025-01_06-01_31-celsius-units.grib"
] 

destination_dir = 'data/ERA5_SINGLE/tratados'
os.makedirs(destination_dir, exist_ok=True)

for file_path in files_to_process:
    filename = os.path.basename(file_path)

    # --- Passo 1: calcular média mensal ---
    monthlymean_file = os.path.join(destination_dir, f"monmean_{filename}")
    command = f"cdo -monmean {file_path} {monthlymean_file}"
    subprocess.run(command, shell=True)
    
    # --- Passo 2: gerar CSV com outputtab para ponto específico ---
    csv_file = os.path.join(destination_dir, filename.replace('.grib', '_monthly.csv'))
    command = (
        f"cdo -outputtab,date,lon,lat,value "
        f"-remapnn,lon=-50.900466_lat=-21.164700 {monthlymean_file} "
        f"| tr -s ' ' ',' > {csv_file}"
    )
    subprocess.run(command, shell=True)
    
    # --- Passo 3: limpar CSV (remover segunda linha e primeira/última coluna) ---
    df = pd.read_csv(csv_file, skiprows=[1])
    df = df.iloc[:, 1:-1]  # remove primeira e última coluna
    df.to_csv(csv_file, index=False)
    
    print(f"Média diária processada e salva: {csv_file}")
