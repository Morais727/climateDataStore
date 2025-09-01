import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# === Abrir dataset ===
ds = xr.open_dataset("data/2025/daily_mean/reanalysis-era5-land_skin_temperature_2025-01-01_daily.nc")

# Selecionar variável
t2m = ds["skt_C"]

# === Criar figura com projeção geográfica ===
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={"projection": ccrs.PlateCarree()})

# Plotar campo (primeiro timestep)
t2m.isel(valid_time=0).plot(
    ax=ax,
    transform=ccrs.PlateCarree(),  # sistema de coordenadas dos dados
    cmap="coolwarm",
    cbar_kwargs={"label": "°C"}
)

# === Adicionar camadas de mapa ===
ax.add_feature(cfeature.COASTLINE, linewidth=1)
ax.add_feature(cfeature.BORDERS, linewidth=0.8, edgecolor="black")

# === Limitar para o Brasil ===
ax.set_extent([-74, -34, -33.7, 5.3], crs=ccrs.PlateCarree())

# Título
plt.title("Temperatura da Superfície (°C) - ERA5-Land\nCom fronteiras do Brasil", fontsize=14)

plt.show()
