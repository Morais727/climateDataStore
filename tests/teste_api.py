import logging
import time
import cdsapi

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="download_era5.log",  
    filemode="w"                    # "w" sobrescreve a cada execução, "a" acrescenta
)
variaveis = ["2m_temperature","total_precipitation"]
for variavel in variaveis:
    logging.info(f"Variável solicitada: {variavel}")
    dataset = "reanalysis-era5-land"
    request = {
                    "variable": [
                                    variavel
                                ],
                    "year": "2024",
                    "month": "01",
                    "day": [
                                "01", "02", "03",
                                "04", "05", "06",
                                "07"
                            ],
                    "time": [
                                "00:00", "01:00", "02:00",
                                "03:00", "04:00", "05:00",
                                "06:00", "07:00", "08:00",
                                "09:00", "10:00", "11:00",
                                "12:00", "13:00", "14:00",
                                "15:00", "16:00", "17:00",
                                "18:00", "19:00", "20:00",
                                "21:00", "22:00", "23:00"
                            ],
                    "data_format": "grib",
                    "download_format": "unarchived",
                    "area": [5.3, -74, -34, -34]
                }

    logging.info("Iniciando conexão com o CDS API")
    client = cdsapi.Client()

    logging.info(f"Iniciando o download do dataset: {dataset}")
    logging.info(f"Período solicitado: {request['year']}-{request['month']} dias {request['day']}")
    logging.info(f"Área geográfica: {request['area']}")
    logging.info(f"Número de variáveis solicitadas: {len(request['variable'])}")

    # Medir tempo
    start_time = time.time()

    try:
        target = f"tests/comparacao/dados/teste_{variavel}_reanalysis_era5_land_jan_2024.grib"
        client.retrieve(dataset, request).download(target)
        elapsed_time = time.time() - start_time
        logging.info(f"Download concluído com sucesso em {elapsed_time:.2f} segundos")
    except Exception as e:
        elapsed_time = time.time() - start_time
        logging.error(f"Falha no download após {elapsed_time:.2f} segundos - Erro: {e}")
