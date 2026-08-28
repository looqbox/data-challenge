import pandas as pd
from sqlalchemy import text
from db_connection import engine


def retrieve_data(product_code=None, store_code=None, date=None):
   
    if product_code is not None and not isinstance(product_code, int):
        raise TypeError(f"product_code must be an integer. Received: {type(product_code).__name__}")

    if store_code is not None and not isinstance(store_code, int):
        raise TypeError(f"store_code must be an integer. Received: {type(store_code).__name__}")

    if date is not None:
        if not isinstance(date, list):
            raise TypeError(f"date must be a list. Received: {type(date).__name__}")
        if len(date) == 0 or len(date) > 2:
            raise ValueError("date must contain 1 or 2 dates: ['YYYY-MM-DD'] or ['YYYY-MM-DD', 'YYYY-MM-DD']")
        if len(date) == 1:
            date = [date[0], date[0]] 

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
        query += " AND DATE BETWEEN :start_date AND :end_date"
        params["start_date"] = date[0]
        params["end_date"] = date[1]

    try:
        with engine.connect() as conn:
            df = pd.read_sql(text(query), conn, params=params)
        return df

    except Exception as e:
        print(f"❌ Query failed: {e}")
        return pd.DataFrame()
    