import pandas as pd
import pymysql
import matplotlib.pyplot as plt
conn = pymysql.connect(
    host="35.199.115.174",
    user="looqbox-challenge",
    password="looq-challenge",
    database="looqbox-challenge",
    port=3306
)

def retrieve_data(product_code, store_code, date):
    """
    Retrieves product sales data filtered by product, store and date range.

    Parameters
    ----------
    product_code : int
        Product code.

    store_code : int
        Store code.

    date : list
        List containing start and end dates.
        Example:
        ['2019-01-01','2019-01-31']

    Returns
    -------
    pandas.DataFrame
    """

    query = f"""
        SELECT *
        FROM data_product_sales
        WHERE PRODUCT_CODE = {product_code}
          AND STORE_CODE = {store_code}
          AND DATE BETWEEN '{date[0]}' AND '{date[1]}'
    """

    df = pd.read_sql(query, conn)

    return df