# casos em python 
# criar função dinamica em python para gerar consultas e retornar dataframes
# product_code (codigo do produto): int
# store_code (codigo da loja): int
# date (data): list
# retornar todas as colunas de data_product_sales

# uma query de base e demais filtros como condições. 

import mysql.connector 
import pandas as pd 

def get_connection():
    return mysql.connector.connect(
        host= "35.199.115.174",
        user= "looqbox-challenge",
        password= "looq-challenge",
        database= "looqbox-challenge"

    )

def retrieve_data(product_code= None, store_code= None, date_range= None):
    query = """
    SELECT *
    FROM `looqbox-challenge`.data_product_sales
    WHERE 1=1
    """

    if product_code:
        query += f" AND PRODUCT_CODE = {product_code}"

    if store_code:
        query += f" AND STORE_CODE = {store_code}"

    if date_range:
        start, end = date_range
        query += f" AND DATE BETWEEN '{start}' AND '{end}'"

    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    
    return df


# saídas 

if __name__ == "__main__":
    df = retrieve_data()
    print(df.head())
