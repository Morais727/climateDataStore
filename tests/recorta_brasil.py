# === Ler shapefile do Brasil 2024 ===
brasil = gpd.read_file("utils/BR_Pais_2024/BR_Pais_2024.shp")

# Reprojetar para WGS84 (ERA5 usa EPSG:4326)
brasil = brasil.to_crs("EPSG:4326")

# === Abrir dataset final (já convertido para Celsius) ===
ds_final = xr.open_dataset(output_nc)  # ou o arquivo diário, se preferir

# Escrever CRS no NetCDF (ERA5 é latitude/longitude)
ds_final = ds_final.rio.write_crs("EPSG:4326")

# === Recortar dados usando shapefile do Brasil ===
ds_brasil = ds_final.rio.clip(brasil.geometry, brasil.crs)

# === Salvar em novo arquivo NetCDF ===
output_br = output_nc.replace(".grib", "_brasil.grib")
ds_brasil.to_netcdf(output_br)

logging.info(f"Arquivo recortado para o Brasil salvo em: {output_br}")