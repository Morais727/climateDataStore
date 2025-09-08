import os
import glob
import pandas as pd

def parquet_para_csv(diretorio_entrada, diretorio_saida=None):
    """
    Converte todos os arquivos .parquet em um diretório para .csv.

    :param diretorio_entrada: pasta onde estão os arquivos .parquet
    :param diretorio_saida: pasta para salvar os arquivos .csv. Se None, salva na mesma pasta
    """
    if diretorio_saida is None:
        diretorio_saida = diretorio_entrada
    os.makedirs(diretorio_saida, exist_ok=True)

    arquivos_parquet = glob.glob(os.path.join(diretorio_entrada, "*.parquet"))
    
    for arquivo in arquivos_parquet:
        df = pd.read_parquet(arquivo)
        nome_arquivo = os.path.basename(arquivo).replace(".parquet", ".csv")
        caminho_saida = os.path.join(diretorio_saida, nome_arquivo)
        df.to_csv(caminho_saida, index=False)
        print(f"Convertido: {arquivo} -> {caminho_saida}")

# Exemplo de uso
if __name__ == "__main__":
    parquet_para_csv("data/2m_temperature/2024")  # pasta de entrada
