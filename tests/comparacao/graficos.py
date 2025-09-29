import xarray as xr
import matplotlib.pyplot as plt

# Caminhos dos arquivos
caminho_zarr = "tests/comparacao/dados/daily_tp_mm"
caminho_nc = "tests/comparacao/dados/daily-tp_mm.nc"

# --- Abre os datasets ---
ds_zarr = xr.open_zarr(caminho_zarr)
ds_nc = xr.open_dataset(caminho_nc, engine="cfgrib")

print("Variáveis no Zarr:", list(ds_zarr.data_vars.keys()))
print("Variáveis no GRIB:", list(ds_nc.data_vars.keys()))

# Nome da variável em cada arquivo
variavel_zarr = "tp"
variavel_nc = "tp"

da_zarr = ds_zarr[variavel_zarr]
da_nc = ds_nc[variavel_nc]

# --- Calcula séries temporais ---
serie_zarr = da_zarr.mean(dim=[d for d in da_zarr.dims if d != "time"])
# Para GRIB: a dimensão de tempo costuma ser 'time' ou 'valid_time'
dim_tempo = "time" if "time" in da_nc.dims else "valid_time"
serie_nc = da_nc.mean(dim=[d for d in da_nc.dims if d != dim_tempo])

# --- Gráfico comparativo ---
plt.figure(figsize=(10, 6))
serie_zarr.plot(label="Zarr (tp)", linestyle="-")
serie_nc.plot(label="GRIB (tp)", linestyle="--")

plt.title("Comparação precipitação diária (tp)")
plt.xlabel("Tempo")
plt.ylabel("Precipitação (mm)")  # ajuste conforme unidade
plt.legend()

plt.savefig("tests/comparacao/dados/graficos/comparacao_daily_tp_mm.png")
plt.show()
