import xarray as xr
import pandas as pd
import numpy as np

# Abrir o NetCDF
ds = xr.open_dataset("saida.nc")

# Obter latitudes e longitudes
latitudes = ds.latitude.values
longitudes = ds.longitude.values

# Criar malha 2D de lat/lon consistente
lon_grid, lat_grid = np.meshgrid(longitudes, latitudes)

# Transformar em DataFrame
df = pd.DataFrame({
    "latitude": lat_grid.ravel(),
    "longitude": lon_grid.ravel()
})

# Salvar em CSV
df.to_csv("latlon-chirps-v2.0.2025.csv", index=False)
