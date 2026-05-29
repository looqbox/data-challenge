import pandas as pd
from sqlalchemy import create_engine, text
from config import DATABASE_URL

# conexão com banco
engine = create_engine(DATABASE_URL)

# query 1
query_store = """
SELECT
    STORE_CODE,
    STORE_NAME,
    START_DATE,
    END_DATE,
    BUSINESS_NAME,
    BUSINESS_CODE
FROM data_store_cad
"""

# query 2
query_sales = """
SELECT
    STORE_CODE,
    DATE,
    SALES_VALUE,
    SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
"""

# executa as queries
df_store = pd.read_sql_query(text(query_store), con=engine)
df_sales = pd.read_sql_query(text(query_sales), con=engine)

# garante que date está como data
df_sales["DATE"] = pd.to_datetime(df_sales["DATE"])

# filtro solicitado no case
df_sales = df_sales[
    (df_sales["DATE"] >= "2019-10-01") &
    (df_sales["DATE"] <= "2019-12-31")
]

# agrupa vendas por loja
df_sales_grouped = (
    df_sales
    .groupby("STORE_CODE", as_index=False)
    .agg({
        "SALES_VALUE": "sum",
        "SALES_QTY": "sum"
    })
)

# calcula TM
df_sales_grouped["TM"] = df_sales_grouped["SALES_VALUE"] / df_sales_grouped["SALES_QTY"]

# junta cadastro de lojas com vendas
df_final = pd.merge(
    df_store,
    df_sales_grouped,
    on="STORE_CODE",
    how="inner"
)

# monta visualização final
df_final = df_final[["STORE_NAME", "BUSINESS_NAME", "TM"]]

df_final = df_final.rename(columns={
    "STORE_NAME": "Loja",
    "BUSINESS_NAME": "Categoria"
})

df_final["TM"] = df_final["TM"].round(2)

df_final = df_final.sort_values("Loja")

print(df_final)
