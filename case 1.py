import os
from typing import Optional, Sequence

import pandas as pd
from sqlalchemy import create_engine, text


def _get_engine():
    host = os.environ["DB_HOST"]
    port = os.environ.get("DB_PORT", "3306")
    user = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]
    database = os.environ["DB_NAME"]
    url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    return create_engine(url)


def retrieve_data(
    product_code: Optional[int] = None,
    store_code: Optional[int] = None,
    date: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    """
    Retrieve rows from data_product_sales filtered by any combination of
    product_code, store_code, and a date range.

    Parameters
    ----------
    product_code : int, optional
        Exact PRODUCT_CODE to filter on.
    store_code : int, optional
        Exact STORE_CODE to filter on.
    date : sequence of two ISO date strings, optional
        [start_date, end_date], inclusive on both ends,
        e.g. ['2019-01-01', '2019-01-31'].

    Returns
    -------
    pd.DataFrame
        All columns from data_product_sales matching the given filters.
        No filters given -> full table.
    """
    if product_code is not None and not isinstance(product_code, int):
        raise TypeError("product_code must be an int")
    if store_code is not None and not isinstance(store_code, int):
        raise TypeError("store_code must be an int")
    if date is not None and len(date) != 2:
        raise ValueError("date must be a list of exactly 2 ISO date strings")

    conditions = []
    params = {}

    if product_code is not None:
        conditions.append("PRODUCT_CODE = :product_code")
        params["product_code"] = product_code

    if store_code is not None:
        conditions.append("STORE_CODE = :store_code")
        params["store_code"] = store_code

    if date is not None:
        conditions.append("DATE BETWEEN :start_date AND :end_date")
        params["start_date"] = date[0]
        params["end_date"] = date[1]

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    query = f"SELECT * FROM data_product_sales {where_clause}"

    engine = _get_engine()
    return pd.read_sql(text(query), engine, params=params)
