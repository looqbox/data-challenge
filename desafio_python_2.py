# Desafio 2: A brand new client sent you two ready-to-go queries...

import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Carrega as variáveis de ambiente
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Monta a string de conexão
connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Cria o motor de conexão
engine = create_engine(connection_string)

# Gera o DataFrame da primeira query fornecida pelo desafio
query_1 = """
    SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
    FROM data_store_cad
    """
df_1 = pd.read_sql(query_1, engine)

# Gera o DataFrame da segunda query fornecida pelo desafio
query_2 = """
    SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
    FROM data_store_sales
    WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
    """
df_2 = pd.read_sql(query_2, engine)

# Faz um INNER JOIN entre os dois DataFrames usando STORE_CODE
merged_df = pd.merge(df_1, df_2, how="inner", on="STORE_CODE")

# Filtra o intervalo de data fornecido pelo desafio ['2019-10-01', '2019-12-31']
merged_df["DATE"] = pd.to_datetime(merged_df["DATE"])
filtered_df = merged_df[(merged_df["DATE"] >= "2019-10-01") & (merged_df["DATE"] <= "2019-12-31")]

# Agrupa pelas colunas STORE_NAME e BUSINESS_NAME, somando os valores de SALES_VALUE e SALES_QTY
grouped_df = (
    filtered_df.groupby(["STORE_NAME", "BUSINESS_NAME"])[
        ["SALES_VALUE", "SALES_QTY"]
    ]
    .sum()
    .reset_index()
)

# Calcula a coluna TM
grouped_df["TM"] = grouped_df["SALES_VALUE"] / grouped_df["SALES_QTY"]
grouped_df["TM"] = grouped_df["TM"].round(2)

# Remove as colunas desnecessárias
final_df = grouped_df[["STORE_NAME", "BUSINESS_NAME", "TM"]]
print(final_df)