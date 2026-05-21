import pandas as pd
from database import get_engine

engine = get_engine()

def recuper_data(product_code=None, store_code=None, date_range=None):
    query = """
    SELECT
        ps.*,
        sc.BUSINESS_NAME
    FROM data_product_sales as ps
    JOIN data_store_cad as sc
        ON ps.STORE_CODE = sc.STORE_CODE
    WHERE 1=1
    """
    params = {}

    if product_code is not None:
        query += " AND ps.PRODUCT_CODE = %(product_code)s"
        params['product_code'] = product_code

    if store_code is not None:
        query += " AND ps.STORE_CODE = %(store_code)s"
        params['store_code'] = store_code
    
    if date_range is not None:
        query += " AND ps.DATE BETWEEN %(start_date)s AND %(end_date)s"
        params['start_date'] = date_range[0]
        params['end_date'] = date_range[1]
    
    return pd.read_sql_query(query, engine, params=params)