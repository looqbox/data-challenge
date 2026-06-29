# Filtragem dos dados baseada nas duas consultas e trazer uma visualização dos dados
# a primeira consulta traz informações das lojas e a segunda traz as informações de vendas 

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


def get_connection():
    return mysql.connector.connect(
        host="35.199.115.174",
        user="looqbox-challenge",
        password="looq-challenge",
        database="looqbox-challenge"
    )


conn = get_connection()


df_store = pd.read_sql("""
    SELECT
        STORE_CODE,
        STORE_NAME,
        START_DATE,
        END_DATE,
        BUSINESS_NAME,
        BUSINESS_CODE
    FROM data_store_cad
""", conn)


df_sales = pd.read_sql("""
    SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
    FROM data_store_sales
    WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
""", conn)


# fazendo merge das consultas 
df = df_sales.merge(df_store, on="STORE_CODE", how="left")

df["DATE"] = pd.to_datetime(df["DATE"])

start = pd.to_datetime("2019-10-01")
end = pd.to_datetime("2019-12-31")

df = df[(df["DATE"] >= start) & (df["DATE"] <= end)]

df["TM"] = df["SALES_VALUE"] / df["SALES_QTY"]


result = df.groupby(
    ["STORE_NAME", "BUSINESS_NAME"]
)["TM"].mean().reset_index()


result.columns = ["Loja", "Categoria", "TM"]
result = result.sort_values("TM", ascending=False)

print(result)


# criando o gráfico
plt.figure(figsize=(10,6))
plt.bar(result["Loja"], result["TM"])
plt.xticks(rotation=45)
plt.title("Ticket Médio por loja")
plt.tight_layout()
plt.show()


conn.close()