import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def retrieve_data(product_code=None, store_code=None, date=None):
    """
    Retrieve data_product_sales filtered by product_code (int or list),
    store_code and date. Returns a DataFrame.
    """
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT", 3306),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
    )

    try:
        conditions = []
        values = []

        if product_code is not None:
            if isinstance(product_code, (list, tuple)):
                placeholders = ", ".join(["%s"] * len(product_code))
                conditions.append(f"PRODUCT_CODE IN ({placeholders})")
                values.extend(product_code)
            else:
                conditions.append("PRODUCT_CODE = %s")
                values.append(product_code)

        if store_code is not None:
            conditions.append("STORE_CODE = %s")
            values.append(store_code)

        if date is not None:
            conditions.append("`DATE` BETWEEN %s AND %s")
            values.append(date[0])
            values.append(date[1])

        query = "SELECT * FROM data_product_sales"

        if conditions:
            query = query + " WHERE " + " AND ".join(conditions)

        df = pd.read_sql_query(query, conn, params=values)
        return df

    finally:
        conn.close()