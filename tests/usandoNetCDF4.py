from netCDF4 import Dataset

ds = Dataset("data/2025/daily.nc", "r")

print(ds.variables.keys())  # ['valid_time', 'valid_time_bnds', 'longitude', 'latitude', 'skt_C']

skt = ds.variables["skt_C"]

print(skt.shape)     # (tempo, lat, lon)
print(skt[0,:,:])    # primeira grade
