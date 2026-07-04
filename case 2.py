import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine


def _get_engine():
    host = os.environ["DB_HOST"]
    port = os.environ.get("DB_PORT", "3306")
    user = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]
    database = os.environ["DB_NAME"]
    url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    return create_engine(url)


QUERY_1 = """
SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
FROM data_store_cad
"""

QUERY_2 = """
SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
"""

engine = _get_engine()
df_store = pd.read_sql(QUERY_1, engine)
df_sales = pd.read_sql(QUERY_2, engine)

# Filtro do período pedido pelo cliente ['2019-10-01','2019-12-31'],
# feito em pandas -- a query 2 não pode ser modificada.
df_sales["DATE"] = pd.to_datetime(df_sales["DATE"])
df_sales = df_sales[
    (df_sales["DATE"] >= "2019-10-01") & (df_sales["DATE"] <= "2019-12-31")
]

merged = df_sales.merge(df_store, on="STORE_CODE", how="left")

agg = (
    merged.groupby(["STORE_NAME", "BUSINESS_NAME"], as_index=False)
    .agg(SALES_VALUE=("SALES_VALUE", "sum"), SALES_QTY=("SALES_QTY", "sum"))
)
agg["TM"] = agg["SALES_VALUE"] / agg["SALES_QTY"]
agg = agg.sort_values("STORE_NAME")

# --- Visualização ---
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=agg, x="STORE_NAME", y="TM", hue="BUSINESS_NAME", ax=ax)
ax.set_xlabel("Loja")
ax.set_ylabel("Ticket Médio (TM)")
ax.set_title("Ticket Médio por Loja (Out-Dez 2019)")
plt.xticks(rotation=45, ha="right")
ax.legend(title="Categoria")

plt.tight_layout()
plt.savefig("ticket_medio_por_loja.png", dpi=150)
plt.show()