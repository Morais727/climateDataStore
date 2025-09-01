import xarray as xr
import pandas as pd
from pathlib import Path

def convert_kelvin_to_celsius(input_nc: str, output_nc: str, output_csv: str):
    """
    Converte variáveis em Kelvin para Celsius em um arquivo NetCDF
    e exporta resultados para NetCDF e CSV.
    """

    # Carrega o arquivo NetCDF
    ds = xr.open_dataset(input_nc)
    new_vars = {}

    for var in ds.data_vars:
        da = ds[var]

        # Verifica se a variável tem atributo "units" = Kelvin
        if "units" in da.attrs and da.attrs["units"] in ["K", "kelvin", "Kelvin"]:
            print(f"✔ Convertendo {var} de Kelvin para Celsius")

            # Converte valores
            da_c = da - 273.15

            # Ajusta atributos
            da_c.attrs["units"] = "°C"
            da_c.name = var + "_C"

            new_vars[var + "_C"] = da_c
        else:
            # Mantém variável original
            new_vars[var] = da

    # Cria novo dataset com variáveis convertidas
    ds_new = xr.Dataset(new_vars, attrs=ds.attrs)

    # Salva em NetCDF
    ds_new.to_netcdf(output_nc)
    print(f"✅ Arquivo NetCDF salvo em: {output_nc}")

    # Converte para CSV (médias espaciais por tempo, para não gerar arquivo gigante)
    df = ds_new.mean(dim=[d for d in ds_new.dims if d not in ["time"]]).to_dataframe()
    df.reset_index(inplace=True)
    df.to_csv(output_csv, index=False)
    print(f"✅ Arquivo CSV salvo em: {output_csv}")

if __name__ == "__main__":
    # Exemplo de uso
    input_file = "data/input.nc"
    output_nc = "data/output_celsius.nc"
    output_csv = "data/output_celsius.csv"

    Path("data").mkdir(exist_ok=True)

    convert_kelvin_to_celsius(input_file, output_nc, output_csv)
