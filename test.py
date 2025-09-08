import xarray as xr

arquivo = "data/2m_temperature/2024/hourly/reanalysis_era5_land-2m_temperature-2024-01_12-01_31.grib"
ds = xr.open_dataset(arquivo, engine="cfgrib")

print(ds.data_vars)
