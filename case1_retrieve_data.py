import pandas as pd
from sqlalchemy import text
from db import get_engine

engine = get_engine()   # criado UMA vez, reusado em toda chamada


def retrieve_data(product_code=None, store_code=None, date=None):
    # STORE_CODE é varchar na tabela; convertemos para str para garantir o match.
    store_code_param = None if store_code is None else str(store_code)

    filtros = [
        (product_code, "PRODUCT_CODE = :pcode", {"pcode": product_code}),
        (store_code,   "STORE_CODE = :scode",   {"scode": store_code_param}),
    ]

    ativos = [f for f in filtros if f[0] is not None]

    if date is not None:
        if not isinstance(date, (list, tuple)) or len(date) != 2:
            raise ValueError(
                "date deve ser uma lista com exatamente 2 elementos: [inicio, fim]."
            )
        ativos.append(
            (date, "DATE BETWEEN :ini AND :fim", {"ini": date[0], "fim": date[1]})
        )

    if not ativos:
        raise ValueError(
            "Informe ao menos um filtro: product_code, store_code ou date."
        )

    where = "WHERE " + " AND ".join(trecho for _, trecho, _ in ativos)

    params = {}
    for _, _, p in ativos:
        params.update(p)

    query = f"SELECT * FROM data_product_sales {where}"
    return pd.read_sql(text(query), engine, params=params)

if __name__ == "__main__":
    print(retrieve_data(product_code=67108).head())
    print(retrieve_data(store_code=1, date=['2019-10-01','2019-12-31']).head())

