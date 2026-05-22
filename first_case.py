
# Desenvolvi o código com a ideia de fazer uma query fixa e depois utilizei alguns "CASES" para identificar se foi passado algum parametro ou não
# e assim montar a query dinamicamente, concatenando a parte necessária para o resultado final.

# Utilizei o ChatGPT para me ajudar a debbugar o codigo apenas.

import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "mysql+pymysql://looqbox-challenge:looq-challenge@35.199.115.174:3306/looqbox-challenge"
)

def retrieve_data(product_code=None, store_code=None, date=None):

    query = """
        SELECT *
        FROM data_product_sales
        WHERE 1=1
    """

    params = {}

    if product_code is not None:
        query += " AND PRODUCT_CODE = :product_code"
        params["product_code"] = product_code

    if store_code is not None:
        query += " AND STORE_CODE = :store_code"
        params["store_code"] = store_code

    if date is not None:
        query += """
            AND DATE BETWEEN :start_date AND :end_date
        """

        params["start_date"] = date[0]
        params["end_date"] = date[1]

    df = pd.read_sql(text(query), engine, params=params)

    return df

my_data = retrieve_data(
    product_code=18,
    store_code=1,
    date=["2019-01-01", "2019-01-02"]
)

print(my_data.head())