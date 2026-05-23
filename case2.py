from dotenv import load_dotenv
import os
import mysql.connector
import pandas as pd

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
port = os.getenv("DB_PORT")


try:
    conexao = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )
    print("Conexão bem-sucedida!")
except mysql.connector.Error as err:
    print(f"Erro ao conectar ao banco de dados: {err}")
    conexao = None


def manual_query(conexao, query):
    if conexao is None:
        raise ConnectionError("Sem conexão ativa!")

    cursor = conexao.cursor()

    cursor.execute(query)

    result = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]

    return pd.DataFrame(result, columns=columns)

query1 = """
SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
FROM data_store_cad
"""

query2="""
SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
"""
df_query_cad = manual_query(conexao, query1)
df_query_sales = manual_query(conexao, query2)


df_query_sales['DATE'] = pd.to_datetime(df_query_sales['DATE'])

df_query_sales = df_query_sales[
    (df_query_sales['DATE'] >= '2019-10-01') &
    (df_query_sales['DATE'] <= '2019-12-31')
]

df_merged = pd.merge(
    df_query_sales,
    df_query_cad,
    on='STORE_CODE'
)
df_grouped = (
    df_merged.groupby(
        ['STORE_NAME', 'BUSINESS_NAME'],
        as_index=False
    )
    .agg({
        'SALES_VALUE': 'sum',
        'SALES_QTY': 'sum'
    })
)

df_grouped['TM'] = (
    df_grouped['SALES_VALUE'] /
    df_grouped['SALES_QTY']
).round(2)

df_final = df_grouped[[
    'STORE_NAME',
    'BUSINESS_NAME',
    'TM'
]].copy()

df_final = (
    df_grouped[['STORE_NAME', 'BUSINESS_NAME', 'TM']].copy().rename(columns=
    {
        'STORE_NAME': 'Loja',
        'BUSINESS_NAME': 'Categoria'
    })
)

print(df_final)