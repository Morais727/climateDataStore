# Guia Prático para Uso da API do ERA5

## Introdução

Este guia explica, de forma clara e prática, como usar a API do **ERA5** através do **Climate Data Store (CDS)**.  
O ERA5 é um dos principais conjuntos de dados climáticos globais, usado em pesquisas e aplicações de meteorologia, meio ambiente e ciência de dados.

A API permite **automatizar downloads**, selecionar apenas as informações necessárias e integrar os dados diretamente em análises com Python.  
A seguir, explicamos o que é o ERA5, como funciona a API, seus limites e como organizar requisições de forma eficiente.

---

## 1. O que é o ERA5?

O **ERA5** é a quinta geração de reanálises climáticas do **ECMWF** (Centro Europeu de Previsões Meteorológicas a Médio Prazo).

Em termos simples:

- Ele pega **observações do clima real** (estações, satélites, balões, navios etc.).
- Usa um **modelo atmosférico moderno** para "recriar" as condições climáticas passadas.

O resultado é um **banco de dados global, consistente e detalhado**, com informações desde **1940 até o presente**, em **resolução horária** (uma leitura por hora).

---

## 2. Como funciona o repositório `climateDataStore`

O código do repositório segue um fluxo simples e eficiente:

1. **Autenticação**: login na API usando a chave de acesso.
2. **Requisição**: escolha do dataset, variáveis, área geográfica, tempo e formato de saída.
3. **Download**: os dados são salvos em um arquivo `.nc` (NetCDF).
4. **Tratamento**: o arquivo é aberto no Python com `xarray` e convertido para formatos mais fáceis (como `.csv`).

## Instalação

É altamente recomendável utilizar um **ambiente virtual** para este projeto, garantindo que as dependências fiquem isoladas de outras instalações do sistema.

## Criando ambiente virtual com **pyenv**

Se você já tem o [pyenv](https://github.com/pyenv/pyenv) instalado:

```bash
# criar ambiente com Python 3.10 (exemplo)
pyenv virtualenv 3.10.14 climate_env

# ativar o ambiente
pyenv activate climate_env
```

Agora todos os pacotes serão instalados dentro desse ambiente.


## Instalando dependências Python

Com o ambiente ativo, instale os pacotes listados em requirements.txt:

```bash
pip install -r 1-requirements.txt
```

## Principais bibliotecas utilizadas:

cdsapi → cliente oficial do Climate Data Store (CDS)

cdo → wrapper Python para o Climate Data Operators

xarray → manipulação de dados climáticos em NetCDF

netCDF4 → suporte para leitura/escrita de arquivos .nc

## Instalando o CDO (Climate Data Operators)

O pacote cdo do Python depende do binário CDO instalado no sistema.

Linux (Ubuntu/Debian)

```bash
Copiar código
sudo apt-get update
sudo apt-get install cdo
```

---

## 3. Como usar a API

### 3.1 Autenticação

- Crie uma conta no [CDS](https://cds.climate.copernicus.eu).
- Sua chave fica salva em `~/.cdsapirc` ou em um `.env`.
- O `cdsapi.Client()` usa essa chave para autenticar seus pedidos.

### 3.2 Formatos de saída

- **NetCDF (`.nc`)** → Melhor para ciência de dados. Funciona bem com `xarray`.
- **GRIB (`.grib`)** → Formato compacto usado em meteorologia operacional, mas mais difícil de manipular.

---

## 4. Limitações da API

### 4.1 Tamanho máximo por requisição

- Cada pedido em **NetCDF** não pode passar de **20 GB**.
- Se passar disso, a requisição falha.
- **Não existe limite diário** → você pode baixar **100 GB ou mais em um dia**, desde que divida em vários pedidos menores.

### 4.2 O que são _fields_?

Um **field** é uma combinação única de:

- **Variável** (ex: temperatura a 2 m)
- **Nível** (ex: superfície, 850 hPa, etc.)
- **Data/Hora** (ex: 2000-01-01 00:00)

Cada snapshot da grade para essa combinação conta como **1 field**.

**Exemplo prático:**

- Variável: temperatura a 2 m
- 1 mês (30 dias)
- 24 horas por dia

Se adicionar outra variável, dobra o número de fields.

### 4.3 Limite de fields

- ERA5 horário → até **120.000 fields por requisição**
- ERA5 mensal → até **10.000 fields por requisição**
- ERA5-Land → até **12.000 fields por mês**

Se passar disso, a requisição falha com `"Request too large"`.

### 4.4 Tempo de espera

- Pedidos pequenos → **5 a 15 minutos**
- Pedidos grandes, dentro do limite → até **2 a 3 horas**
- Pedidos fora do limite → nunca terminam; precisam ser refeitos em partes menores

### 4.5 Por que os limites mudam entre datasets

| Dataset      | Limite de fields | Por que                                                                                                                               |
| ------------ | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| ERA5 horário | ~120.000         | Cada field é um **snapshot de uma hora**, sem agregação. O servidor só precisa empacotar os arquivos.                                 |
| ERA5 mensal  | ~10.000          | Cada field já é **pré-agregado** (média do mês). O servidor precisa calcular os valores antes de entregar, por isso o limite é menor. |
| ERA5-Land    | ~12.000/mês      | Semelhante ao ERA5 mensal, limitado ao dataset de superfície terrestre.                                                               |

**Exemplo prático:**
 Isso mostra por que o limite de fields é maior no horário do que no mensal: os dados horários são “crus” e fáceis de empacotar, enquanto os mensais já vêm calculados e exigem processamento extra.

---

## 5. Boas práticas

1. **Use a interface web do CDS**

   - Preencha o formulário no site do dataset.
   - Clique em **“Show API request”** → o site gera o código Python pronto.

2. **Divida seus pedidos**

   - Por mês ou por ano.
   - Por poucas variáveis de cada vez.

3. **Baixe apenas o necessário**
   - Defina a área (`area`).
   - Defina o período de interesse.
   - Selecione só as variáveis que vai usar.

---

## 6. Integração no Python

Depois do download (`output.nc`):

```python
import xarray as xr

# Abre o arquivo
ds = xr.open_dataset("output.nc")

# Média da temperatura a 2 m no tempo
mean_temp = ds["t2m"].mean(dim="time")

# Converte para dataframe
df = ds.to_dataframe().reset_index()
```

## 7. Conversão de dados (NetCDF → CSV)

É possível converter arquivos `.nc` para `.csv` utilizando ferramentas como `xarray`, `pandas` ou `cdo`.  
Na prática, essa conversão é viável para **conjuntos pequenos ou médios**, mas **pode se tornar inviável em datasets muito grandes**:

- Os arquivos do ERA5 podem ser **enormes** (milhões de pontos × milhares de timestamps).
- Um único mês global em resolução horária pode gerar **bilhões de linhas** ao ser convertido para CSV.
- O tamanho final do `.csv` pode facilmente chegar a **dezenas ou centenas de GB**, tornando o processamento lento e difícil de manipular.

 **Recomendações práticas:**

- Trabalhar diretamente no formato **NetCDF** (com `xarray`) ou em **Zarr** (otimizado para leitura sob demanda).
- Converter para **CSV** apenas quando for **um ponto específico (lat/lon)** ou um conjunto pequeno de estatísticas (ex: médias regionais, séries temporais em cidades).

---

### Comparação entre `xarray` e `cdo`

Após avaliar as ferramentas, verificou-se que o **xarray é mais flexível, integrado ao Python e mais eficiente** que o `cdo` em tarefas de manipulação e conversão:

- **Integração:**

  - `xarray` funciona diretamente no ecossistema Python, facilitando análises, integrações e automações.
  - `cdo` precisa ser executado manualmente ou via `subprocess`, o que adiciona complexidade ao fluxo.
  - Existe também o pacote [`cdo.py`](https://code.mpimet.mpg.de/projects/cdo/wiki/Cdo%7Epython), que permite chamar os comandos do CDO diretamente no Python, sem `subprocess`. Porém, essa integração ainda depende de arquivos externos e não é tão natural quanto trabalhar com `xarray` em memória.

- **Fluxo de trabalho:**

  - Com `cdo`, cada variável precisa ser convertida separadamente, exigindo um _merge_ posterior dos arquivos.
  - Com `xarray`, todas as variáveis podem ser exportadas de uma só vez com **um único comando**.

- **Desempenho (com base nos testes de execução):**

  - `cdo`: levou entre **92 e 104 segundos** para concluir a conversão.
  - `xarray`: concluiu a mesma tarefa em apenas **14 a 16 segundos**.
  - Resultado: o `xarray` foi até **7× mais rápido** que o `cdo` no cenário testado.

- **Tamanho dos arquivos resultantes:**
  - Arquivo **CSV** (`saida_xarray.csv`): **105,3 MB**
  - Arquivo **NetCDF** (`daily_cdo_celsius.nc`): **14,1 MB**
  - Ou seja, o **NetCDF é cerca de 7,5× mais compacto**, além de manter metadados e estrutura multidimensional.

 **Resumo da comparação:**

| Critério           | xarray (Python)  | cdo (externo)                           |
| ------------------ | ---------------- | --------------------------------------- |
| Integração         | Direta no Python | Requer execução externa/subprocess      |
| Conversão múltipla | Um comando       | Precisa converter variável por variável |
| Velocidade (teste) | 14–16s           | 92–104s                                 |
| Eficiência         | Alta             | Baixa                                   |
| Tamanho CSV        | 105,3 MB         | —                                       |
| Tamanho NetCDF     | 14,1 MB          | —                                       |

---

## 8. Gerenciamento de Requisições com Airflow

Estamos utilizando o **Apache Airflow** para gerenciar o fluxo de requisição de dados climáticos do **ERA5**.  

Criamos uma **DAG** dedicada exclusivamente às requisições, estruturada para:  
- Realizar o processo **mês a mês** (seguindo as boas práticas recomendadas, evitando requisições muito grandes).  
- Garantir maior velocidade e confiabilidade no download dos dados.  

---

## Estrutura de diretórios

Os dados são organizados no seguinte padrão:

data/
└── variavel_de_interesse/
└── ano/
└── arquivos_de_dados.grib

- Para cada mês, será gerado um arquivo `.grib`.  
- Posteriormente, esses arquivos serão tratados e agregados em um único arquivo consolidado.  

---

## Execução em servidor remoto

O processo de requisição e tratamento roda em um **servidor remoto**.  
Para acompanhar a interface do **Airflow** em sua máquina local, utilizamos **túnel SSH** redirecionando a porta **8080** do servidor para a máquina local.

### Comando:

```bash
ssh -L 8080:localhost:8080 usuario@ip_servidor
```

Após executar esse comando, basta acessar no navegador:

http://localhost:8080
e você verá a interface do Airflow rodando no servidor remoto.



## Data citation

This project uses data from the ERA5-Land dataset provided by the
[Copernicus Climate Data Store (CDS)](https://cds.climate.copernicus.eu/),
released under the **Creative Commons Attribution (CC-BY) licence**.

When using this data, please cite as:

Muñoz-Sabater, J. (2019): ERA5-Land hourly data from 1981 to present.
Copernicus Climate Change Service (C3S) Climate Data Store (CDS).
DOI: [10.24381/cds.e9c9c792](https://doi.org/10.24381/cds.e9c9c792).
