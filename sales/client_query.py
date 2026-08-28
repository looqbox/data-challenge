import pandas as pd
from sqlalchemy import text
from db_connection import engine

query1 = """
SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
FROM `looqbox-challenge`.data_store_cad
"""

query2 = """
SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
FROM `looqbox-challenge`.data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
"""

with engine.connect() as conn:
    df_stores = pd.read_sql(text(query1), conn)
    df_sales = pd.read_sql(text(query2), conn)

df_sales['DATE'] = pd.to_datetime(df_sales['DATE'])
df_sales = df_sales[
    (df_sales['DATE'] >= '2019-10-01') &
    (df_sales['DATE'] <= '2019-12-31')
]

df = df_sales.merge(df_stores, on='STORE_CODE', how='inner')

df_result = df.groupby(['STORE_NAME', 'BUSINESS_NAME']).apply(
    lambda x: round(x['SALES_VALUE'].sum() / x['SALES_QTY'].sum(), 2)
).reset_index()

df_result.columns = ['Loja', 'Categoria', 'TM']
df_result = df_result.sort_values('Loja').reset_index(drop=True)

print(df_result.to_string(index=False))