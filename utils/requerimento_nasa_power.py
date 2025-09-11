import requests
import json
import time

# Defina os limites da sua área
lat_start, lat_end = -22, -18
lon_start, lon_end = -52, -47
lat_step = 1  # passo em graus (ajuste para maior resolução)
lon_step = 1

# Datas
start_date = "20240101"
end_date = "20251231"

# Parâmetro de precipitação
parameter = "PRECTOT"
community = "AG"
data_format = "JSON"

# Função para gerar lista de coordenadas
def generate_grid(lat_start, lat_end, lon_start, lon_end, lat_step, lon_step):
    lats = [round(lat, 2) for lat in range(lat_start, lat_end + 1, lat_step)]
    lons = [round(lon, 2) for lon in range(lon_start, lon_end + 1, lon_step)]
    grid = [(lat, lon) for lat in lats for lon in lons]
    return grid

# Gerar grid
grid = generate_grid(lat_start, lat_end, lon_start, lon_end, lat_step, lon_step)

# URL base da API
base_url = "https://power.larc.nasa.gov/api/temporal/hourly/point"

# Dicionário para armazenar todos os dados
all_data = {}

for lat, lon in grid:
    params = {
        "parameters": parameter,
        "community": community,
        "longitude": lon,
        "latitude": lat,
        "start": start_date,
        "end": end_date,
        "format": data_format
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        all_data[f"{lat},{lon}"] = data
        print(f"Dados obtidos para ({lat},{lon})")
        
        # Evitar sobrecarga na API
        time.sleep(1)  # espera 1 segundo entre requisições
    except Exception as e:
        print(f"Erro ao obter dados para ({lat},{lon}): {e}")

# Salvar todos os dados em um arquivo JSON
with open("precipitacao_2024_2025.json", "w") as f:
    json.dump(all_data, f)

print("Download completo!")
