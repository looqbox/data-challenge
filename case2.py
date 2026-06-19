#%%

import pymysql
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

#%%

conn = pymysql.connect(
    host="35.199.115.174",
    user="looqbox-challenge",
    password="looq-challenge"
)

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
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-01'
"""

#%%

df_cad = pd.read_sql(query1, conn)
df_sales = pd.read_sql(query2, conn)

print(df_cad.head())
print(df_sales.head())

#%%

#Utilizei novamente llm aqui pois estava tentando realizar o filtro das datas utilizando >= ou <= sem antes transformar a coluna para date time igual estou fazendo no df abaixo desse comentário
df_sales["DATE"] = pd.to_datetime(df_sales["DATE"])

df_sales = df_sales[(df_sales["DATE"] >= "2019-10-01") & (df_sales["DATE"] <= "2019-12-31")]

df_sales_agg = df_sales.groupby("STORE_CODE")[["SALES_VALUE", "SALES_QTY"]].sum().reset_index()

df_final = df_cad.merge(df_sales_agg, on="STORE_CODE", how="left")

print(df_final)
#%%

#utilizei llm para passar os "parametros" corretos para a criação do gráfico

df_final = df_final.sort_values("SALES_VALUE", ascending=False)

plt.figure(figsize=(12, 6))
plt.bar(df_final["STORE_NAME"], df_final["SALES_VALUE"])
plt.xticks(rotation=45, ha="right")
plt.title("Vendas por Loja - Q4 2019")
plt.ylabel("Total de Vendas")
plt.tight_layout()
plt.show()

