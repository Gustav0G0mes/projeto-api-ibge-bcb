#Inicio

# importação das bibliotecas
import requests
import pandas as pd
from io import StringIO


# API DO IBGE
url_ibge = "https://servicodados.ibge.gov.br/api/v1/bdg/estado/AM/estacoes"
params_ibge = {"Estacoes": 20}

resp_ibge = requests.get(url_ibge, params=params_ibge, timeout=30)
resp_ibge.raise_for_status()

df_ibge = pd.DataFrame(resp_ibge.json())

print("=" * 60)
print("API DO IBGE")
print("=" * 60)
print("Endpoint utilizado:")
print(resp_ibge.url)
print("\nPrimeiras linhas dos dados do IBGE:")
print(df_ibge.head())


# API DO BANCO CENTRAL

# Valores Selic 

url_bcb_json = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados"
params_bcb_json = {"formato": "json",
"dataInicial": "01/01/2020",
"dataFinal": "31/12/2025"}


resp_bcb_json = requests.get(url_bcb_json, params=params_bcb_json, timeout=30)
resp_bcb_json.raise_for_status()
df_bcb_json = pd.DataFrame(resp_bcb_json.json())


print("\n" + "=" * 60)
print("API DO BANCO CENTRAL")
print("=" * 60)
print("Endpoint utilizado:")
print(resp_bcb_json.url)
print("\nPrimeiras linhas dos dados do Banco Central:")
print(df_bcb_json.head())


# 3. EXTRAÇÃO DE TABELA SIMPLES DO BANCO

# Nesta etapa, os dados foram obtidos em formato CSV,

# convertidos em DataFrame e salvos como bcb_tabela.csv.

url_bcb_csv = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados"
params_bcb_csv = {
    "formato": "csv",
    "dataInicial": "01/01/2020",
    "dataFinal": "31/12/2025"}


resp_bcb_csv = requests.get(url_bcb_csv, params=params_bcb_csv, timeout=30)
resp_bcb_csv.raise_for_status()
df_bcb_tabela = pd.read_csv(StringIO(resp_bcb_csv.text), sep=';')


print("\n" + "=" * 60)
print("TABELA PÚBLICA EXTRAÍDA DO BANCO CENTRAL")
print("=" * 60)
print("Primeiras linhas da tabela:")
print(df_bcb_tabela.head())


# salvando o arquivo solicitado
df_bcb_tabela.to_csv("bcb_tabela.csv", index=False, encoding="utf-8-sig")
print("\nArquivo bcb_tabela.csv salvo com sucesso.")


# TRATAMENTO DOS DADOS

# 1. Renomeação das colunas
# 2. Conversão de data para datetime
# 3. Conversão da coluna para numérico
# 4. Remoção de nulos
# 5. Remoção de duplicidades

df_tratado = df_bcb_tabela.copy()


# renomeando colunas
df_tratado.columns = ["data", "valor"]


# ajuste de estilos
df_tratado["data"] = pd.to_datetime(df_tratado["data"], format="%d/%m/%Y", errors="coerce")
df_tratado["valor"] = df_tratado["valor"].astype(str).str.replace(",", ".", regex=False)
df_tratado["valor"] = pd.to_numeric(df_tratado["valor"], errors="coerce")

# removendo nulos
df_tratado = df_tratado.dropna(subset=["data", "valor"])

# removendo duplicidades
df_tratado = df_tratado.drop_duplicates()
print("\n" + "=" * 60)
print("DADOS TRATADOS")
print("=" * 60)
print("Primeiras linhas dos dados tratados:")
print(df_tratado.head())


# VALIDAÇÃO DOS DADOS

print("\n" + "=" * 60)
print("VALIDAÇÃO DOS DADOS")
print("=" * 60)
print("Tipos de dados:")
print(df_tratado.dtypes)
print("\nValores nulos por coluna:")
print(df_tratado.isnull().sum())
print("\nQuantidade de registros duplicados:")
print(df_tratado.duplicated().sum())
print("\nQuantidade final de linhas:")
print(len(df_tratado))
print("\nPeríodo dos dados tratados:")
print("Data mínima:", df_tratado["data"].min())
print("Data máxima:", df_tratado["data"].max())



# 6. EXPORTAÇÃO DOS DADOS 
df_tratado.to_csv("dados_tratados.csv", index=False, encoding="utf-8-sig")
df_tratado.to_parquet("dados_tratados.parquet", index=False)

print("\n" + "=" * 60)
print("ARQUIVOS GERADOS")
print("=" * 60)
print("- bcb_tabela.csv")
print("- dados_tratados.csv")
print("- dados_tratados.parquet")


# 7. RESPOSTAS TEÓRICAS

print("\n" + "=" * 60)
print("RESPOSTAS TEÓRICAS")
print("=" * 60)

print("""
1. Importância do web scraping no ambiente de trabalho
O web scraping é importante porque permite coletar dados públicos da internet
de forma automatizada, reduzindo tarefas manuais e aumentando a produtividade.
Ele pode ser usado para monitoramento de preços, análise de concorrência,
coleta de indicadores e geração de relatórios, ajudando na tomada de decisão
baseada em dados.

      
2. Principais riscos legais e éticos envolvidos
Os principais riscos legais e éticos envolvem:
- descumprimento dos termos de uso dos sites;
- violação de direitos autorais;
- coleta indevida de dados pessoais;
- possíveis problemas relacionados à LGPD;
- excesso de requisições, que pode prejudicar o funcionamento do site.

Duas medidas práticas para mitigação:
1. Verificar os termos de uso do site e priorizar APIs oficiais quando existirem.
2. Coletar apenas os dados necessários, evitando dados pessoais e respeitando
   limites de acesso e frequência de requisições.
3. Diferenças entre requisição via API e requisição sem API
Uma requisição via API acessa dados de forma estruturada, organizada e
documentada, geralmente em formatos como JSON ou CSV. Isso facilita o
tratamento dos dados e torna o processo mais confiável.
Já uma requisição sem API normalmente depende da extração de informações
diretamente de páginas HTML, por meio de web scraping. Essa abordagem tende
a ser mais frágil, pois mudanças no layout do site podem quebrar o código.

      
4. Qual abordagem é mais adequada?
A abordagem mais adequada é a requisição via API, sempre que disponível,
porque ela é mais estável, mais fácil de manter, mais segura e geralmente
mais adequada do ponto de vista técnico e legal. O web scraping pode ser útil
quando não existe API, mas exige mais cuidado.
""")
print("Execução finalizada com sucesso.")

#fim