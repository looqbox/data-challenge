
# Desenvolvi o código utilizando as duas Queries que estavam no desafio, e depois utilizei o pandas para fazer a junção dos dados.

# Utilizei o ChatGPT para me ajudar a debbugar o codigo apenas.


import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://looqbox-challenge:looq-challenge@35.199.115.174:3306/looqbox-challenge"
)

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

query_2 = """
SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
"""

df_store = pd.read_sql(query_1, engine)

df_sales = pd.read_sql(query_2, engine)

df_sales["DATE"] = pd.to_datetime(df_sales["DATE"])

df_sales = df_sales[
    (df_sales["DATE"] >= "2019-10-01") &
    (df_sales["DATE"] <= "2019-12-31")
]

df_final = df_sales.merge(
    df_store,
    on="STORE_CODE",
    how="left"
)

df_grouped = (
    df_final
    .groupby(
        ["STORE_NAME", "BUSINESS_NAME"],
        as_index=False
    )
    .agg({
        "SALES_VALUE": "sum",
        "SALES_QTY": "sum"
    })
)

df_grouped["TM"] = (
    df_grouped["SALES_VALUE"] /
    df_grouped["SALES_QTY"]
).round(2)

result = df_grouped[
    ["STORE_NAME", "BUSINESS_NAME", "TM"]
]

result = result.rename(columns={
    "STORE_NAME": "Loja",
    "BUSINESS_NAME": "Categoria"
})

print(result)
