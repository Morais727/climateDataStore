# import cdsapi

# c = cdsapi.Client()

# c.retrieve(
#     'reanalysis-era5-single-levels',
#     {
#         'product_type': 'reanalysis',
#         'variable': '2m_temperature',
#         'year': '2025',
#         'month': '01',
#         'day': '01',
#         'time': [
#                   '00:00', '06:00', '12:00', '18:00',
#                 ],
#         "download_format": "unarchived",
#         "area": [90, -180, -90, 180],
#         'format': 'netcdf',
#     },
#     'ecmwf/era5_t2m_20250101.nc')

import cdsapi

client = cdsapi.Client()

dataset = 'reanalysis-era5-pressure-levels'
request = {
  'product_type': ['reanalysis'],
  'variable': ['geopotential'],
  'year': ['2024'],
  'month': ['03'],
  'day': ['01'],
  'time': ['13:00'],
  'pressure_level': ['1000'],
  'data_format': 'netcdf',
}
target = 'ecmwf/download.nc'

client.retrieve(dataset, request, target)