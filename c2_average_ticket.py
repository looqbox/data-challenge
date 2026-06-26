import os

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

QUERY_STORES = """
SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
FROM data_store_cad
"""

QUERY_SALES = """
SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
"""

PERIOD_START = "2019-10-01"
PERIOD_END = "2019-12-31"


def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT", 3306),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
    )


def load_data():
    conn = get_connection()
    try:
        stores = pd.read_sql_query(QUERY_STORES, conn)
        sales = pd.read_sql_query(QUERY_SALES, conn)
        return stores, sales
    finally:
        conn.close()


def build_average_ticket(stores, sales):
    sales = sales.copy()
    sales["DATE"] = pd.to_datetime(sales["DATE"])
    mask = (sales["DATE"] >= PERIOD_START) & (sales["DATE"] <= PERIOD_END)
    sales = sales.loc[mask]

    agg = sales.groupby("STORE_CODE", as_index=False)[["SALES_VALUE", "SALES_QTY"]].sum()
    agg["TM"] = (agg["SALES_VALUE"] / agg["SALES_QTY"]).round(2)

    result = agg.merge(
        stores[["STORE_CODE", "STORE_NAME", "BUSINESS_NAME"]],
        on="STORE_CODE",
        how="inner",
    )

    result = result.rename(columns={"STORE_NAME": "Loja", "BUSINESS_NAME": "Categoria"})
    result = result[["Loja", "Categoria", "TM"]].sort_values("Loja").reset_index(drop=True)
    return result


def plot_table(df, path="average_ticket.png"):
    fig, ax = plt.subplots(figsize=(6, 0.4 * len(df) + 1))
    ax.axis("off")

    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.4)

    for col in range(len(df.columns)):
        cell = table[0, col]
        cell.set_facecolor("#2f5496")
        cell.set_text_props(color="white", weight="bold")

    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def main():
    stores, sales = load_data()
    result = build_average_ticket(stores, sales)
    print(result.to_string(index=False))
    path = plot_table(result)
    print(f"\nVisualização salva em: {path}")


if __name__ == "__main__":
    main()
