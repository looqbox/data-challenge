import pandas as pd
from sqlalchemy import text


def retrieve_data(product_code=None, store_code=None, date=None, engine=None):
    if engine is None:
        raise ValueError("Informe uma conexao valida com o banco de dados.")

    query = """
        SELECT *
        FROM data_product_sales
        WHERE 1 = 1
    """

    params = {}

    if product_code is not None:
        query += " AND PRODUCT_CODE = :product_code"
        params["product_code"] = product_code

    if store_code is not None:
        query += " AND STORE_CODE = :store_code"
        params["store_code"] = store_code

    if date is not None:
        if not isinstance(date, list) or len(date) != 2:
            raise ValueError("date deve ser uma lista como ['YYYY-MM-DD', 'YYYY-MM-DD'].")

        query += " AND DATE BETWEEN :start_date AND :end_date"
        params["start_date"] = date[0]
        params["end_date"] = date[1]

    return pd.read_sql(text(query), engine, params=params)


def build_ticket_medio_table(stores, sales):
    sales = sales.copy()
    sales["DATE"] = pd.to_datetime(sales["DATE"])

    vendas_4t = sales[
        (sales["DATE"] >= "2019-10-01") &
        (sales["DATE"] <= "2019-12-31")
    ]

    base = vendas_4t.merge(stores, on="STORE_CODE", how="left")

    result = (
        base.groupby(["STORE_NAME", "BUSINESS_NAME"], as_index=False)
            .agg(
                SALES_VALUE=("SALES_VALUE", "sum"),
                SALES_QTY=("SALES_QTY", "sum")
            )
    )

    result = result[result["SALES_QTY"] != 0].copy()
    result["TM"] = result["SALES_VALUE"] / result["SALES_QTY"]

    result = result.rename(columns={
        "STORE_NAME": "Loja",
        "BUSINESS_NAME": "Categoria"
    })

    result = result[["Loja", "Categoria", "TM"]]
    result["TM"] = result["TM"].round(2)

    return result.sort_values("Loja")
