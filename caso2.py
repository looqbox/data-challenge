"""
Execução do caso 2 filtro por periodo
Autora: Gabriella Pacheco
"""

import pandas as pd
from mysql_conexao import executa_query


QUERY_LOJAS = """
SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
FROM data_store_cad
"""

QUERY_VENDAS = """
SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
"""

def calcula_ticket_medio(date: list) -> pd.DataFrame:

    lojas  = executa_query(QUERY_LOJAS)
    vendas = executa_query(QUERY_VENDAS)

    # Filtrando o periodo desejado pelo cliente
    vendas["DATE"] = pd.to_datetime(vendas["DATE"])
    vendas = vendas[
        (vendas["DATE"] >= date[0]) &
        (vendas["DATE"] <= date[1])
    ]

    vendas_agrupadas = (
        vendas.groupby("STORE_CODE")
        .agg(SALES_VALUE=("SALES_VALUE", "sum"), SALES_QTY=("SALES_QTY", "sum"))
        .reset_index()
    )

    # Juntando as informacoes
    df = vendas_agrupadas.merge(lojas[["STORE_CODE", "STORE_NAME", "BUSINESS_NAME"]], on="STORE_CODE")

    # ticket medio do caso
    df["TM"] = (df["SALES_VALUE"] / df["SALES_QTY"]).round(2)

    resultado = (
        df[["STORE_NAME", "BUSINESS_NAME", "TM"]]
        .rename(columns={"STORE_NAME": "Loja", "BUSINESS_NAME": "Categoria"})
        .sort_values("Loja")
        .reset_index(drop=True)
    )

    return resultado

if __name__ == "__main__":
    date = ["2019-10-01", "2019-12-31"]

    df = calcula_ticket_medio(date)
    print(df.to_string(index=False))