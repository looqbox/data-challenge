# pylint : disable=line-too-long
# 2) Um novo cliente lhe enviou duas consultas prontas para serem respondidas. Elas estão listadas abaixo:

import pandas as pd
from src.conexao_db import get_engine

engine = get_engine()

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#= CONSULTAS #=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

consulta_1 = """
SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
FROM data_store_cad
"""

consulta_2 = """
SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
"""

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#= MERGE DAS CONSULTAS #=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

df1 = pd.read_sql(consulta_1, engine)
df2 = pd.read_sql(consulta_2, engine)

merge_consultas = df1.merge(df2, on="STORE_CODE", how="inner")

df_final = (
    merge_consultas
    .groupby(["STORE_NAME", "BUSINESS_NAME"], as_index=False)
    .agg({
        "SALES_VALUE": "sum",
        "SALES_QTY": "sum"
    })
)

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#= TRATAMENTO #=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

df_final["TM"] = (df_final["SALES_VALUE"] / df_final["SALES_QTY"]).round(2)

df_final = df_final.rename(columns={
    'STORE_NAME': 'Loja',
    'BUSINESS_NAME': 'Categoria'
})

df_final = df_final[["Loja", "Categoria", "TM"]].to_string(index=False)

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#= RESULTADOS #=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

print("\nQuestão 2:")
print(df_final)

