import xarray as xr
import matplotlib.pyplot as plt

# abrir o arquivo NetCDF/GRIB convertido
ds = xr.open_dataset("data/2025/reanalysis-era5-land_skin_temperature_2025-01-01_celsius.nc")

print(ds)

# selecionar a variável de interesse
t2m = ds['skt_C']
print(t2m)

# pegar os valores como numpy array
arr = t2m.values

# # acessar um tempo específico (aqui ajustei para 'valid_time')
# t2m_12utc = t2m.sel(valid_time="2025-01-01T12:00")
# print(t2m_12utc)

# plotar o primeiro campo de tempo
t2m.isel(valid_time=0).plot()
plt.show()
