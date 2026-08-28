"""Reusable retrieval function for Case 1."""

from collections.abc import Sequence
from datetime import date

import pandas as pd
from sqlalchemy import Engine, text


def retrieve_data(
    engine: Engine,
    product_code: int | None = None,
    store_code: int | None = None,
    date_range: Sequence[str] | None = None,
) -> pd.DataFrame:
    """Return product sales using optional, safely parameterized filters."""
    clauses: list[str] = []
    parameters: dict[str, object] = {}

    if product_code is not None:
        clauses.append("PRODUCT_CODE = :product_code")
        parameters["product_code"] = product_code
    if store_code is not None:
        clauses.append("STORE_CODE = :store_code")
        parameters["store_code"] = store_code
    if date_range is not None:
        if len(date_range) != 2:
            raise ValueError("date_range must contain exactly a start date and an end date")
        start_date, end_date = (date.fromisoformat(value) for value in date_range)
        if start_date > end_date:
            raise ValueError("date_range start date cannot be after the end date")
        clauses.append("DATE BETWEEN :start_date AND :end_date")
        parameters.update(start_date=start_date, end_date=end_date)

    query = "SELECT * FROM data_product_sales"
    if clauses:
        query += " WHERE " + " AND ".join(clauses)

    return pd.read_sql_query(text(query), engine, params=parameters)
