import pandas as pd
from sqlalchemy import text
from db import get_engine

engine = get_engine()

query_lojas = text("""
SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
FROM data_store_cad
""")

query_vendas = text("""
SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
""")

df_lojas = pd.read_sql(query_lojas, engine)
df_vendas = pd.read_sql(query_vendas, engine)

# 1. Garantir datetime
df_vendas["DATE"] = pd.to_datetime(df_vendas["DATE"])

# 2. Filtrar Q4 (restrição: não modificar a query, filtra aqui)
q4 = df_vendas[
    (df_vendas["DATE"] >= "2019-10-01") &
    (df_vendas["DATE"] <= "2019-12-31")
]

# 3. Agregar por loja
agg = q4.groupby("STORE_CODE").agg(
    valor_total=("SALES_VALUE", "sum"),
    qtd_total=("SALES_QTY", "sum"),
).reset_index()

# 4. Ticket Médio
agg["TM"] = (agg["valor_total"] / agg["qtd_total"]).round(2)

# 5. Merge com lojas
final = agg.merge(df_lojas, on="STORE_CODE")

# 6. Tabela final
resultado = final[["STORE_NAME", "BUSINESS_NAME", "TM"]]
resultado.columns = ["Loja", "Categoria", "TM"]

# 7. Ordenar por Loja
resultado = resultado.sort_values("Loja").reset_index(drop=True)

print(resultado)
