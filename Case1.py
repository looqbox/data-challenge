#%%

import pymysql
import pandas as pd

#%%
#Utilizei 2x o chatgpt uma foi para relebrar como efetuava essas conexões a base de dados e outra é porque estava retornando erro de acesso negado porém era um erro de sintaxe
def retrieve_data(product_code=None, store_code=None, date=None):

    conn = pymysql.connect(
        host="35.199.115.174",
        user="looqbox-challenge",
        password="looq-challenge"
    )

    query = "SELECT * FROM `looqbox-challenge`.data_product_sales WHERE 1=1"

    if product_code:
        query += f" AND PRODUCT_CODE = {product_code}"

    if store_code:
        query += f" AND STORE_CODE = '{store_code}'"  # string, precisa de aspas

    if date:
        query += f" AND DATE BETWEEN '{date[0]}' AND '{date[1]}'"

    print(f"Query gerada: {query}")

    df = pd.read_sql(query, conn)
    conn.close()

    return df

#%%

my_data = retrieve_data(product_code=18, store_code=1, date=["2019-01-01", "2019-01-31"])
print(my_data)