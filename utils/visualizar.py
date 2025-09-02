import xarray as xr
import geopandas as gpd
import rioxarray
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# === Abrir NetCDF (ajuste o caminho para o seu arquivo ERA5) ===
ds = xr.open_dataset("/home/marcos-morais/Documentos/ZETTA/climateDataStore/data/2025/hourly/reanalysis-era5-land_2m_dewpoint_temperature_skin_temperature_2025-01-01_celsius.nc")
t2m = ds["d2m_C"]

# Garantir que tem CRS definido (ERA5 está em lat/lon)
t2m = t2m.rio.write_crs("EPSG:4326")

# === Ler shapefile do Brasil 2024 (IBGE) ===
brasil = gpd.read_file("/home/marcos-morais/Documentos/ZETTA/DOCS/BR_Pais_2024/BR_Pais_2024.shp")

# Conferir CRS do shapefile
print("CRS shapefile:", brasil.crs)   # deve ser EPSG:4674 (SIRGAS 2000)

# Reprojetar shapefile para WGS84 (EPSG:4326), compatível com ERA5
brasil = brasil.to_crs("EPSG:4326")

# === Recortar NetCDF pelo polígono do Brasil ===
t2m_brasil = t2m.rio.clip(brasil.geometry, brasil.crs)

# === Plotar resultado ===
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={"projection": ccrs.PlateCarree()})

t2m_brasil.isel(valid_time=0).plot(
    ax=ax,
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    cbar_kwargs={"label": "°C"}
)

# Fronteira do Brasil
brasil.boundary.plot(ax=ax, edgecolor="black", linewidth=1)

ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor="gray")

plt.title("ERA5-Land – Temperatura 2m (°C)\nRecortado pela fronteira oficial do Brasil (IBGE 2024)", fontsize=14)
plt.show()
