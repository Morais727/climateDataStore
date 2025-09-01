import xarray as xr

ds = xr.open_dataset("data/2025/daily.nc")

print(ds.data_vars)   # lista só as variáveis de dados (ignora coords auxiliares)

skt = ds["skt_C"]

print(skt.mean().item())   # média global
print(skt.sel(valid_time="2025-01-01T11:30:00"))  # dado de um dia

skt.sel(valid_time="2025-01-01T11:30:00").plot()
