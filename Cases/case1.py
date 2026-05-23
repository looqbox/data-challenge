import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://looqbox-challenge:looq-challenge@35.199.115.174:3306/looqbox-challenge"
)

def retrieve_data(product_code = None, store_code = None, date = None):

    aux = []
    where_clause = ''
    
    if product_code:
        aux.append(f'dps.product_code = {product_code}')

    if store_code:
        aux.append(f'dps.store_code = {store_code}')

    if date and len(date) == 2:
        aux.append(f"dps.date BETWEEN '{date[0]}' AND '{date[1]}'")

    if aux:
        where_clause = 'WHERE ' + ' AND '.join(aux)

    query = f"""
    SELECT *
    FROM data_product_sales dps
    {where_clause}
    """

    df = pd.read_sql(query, engine)

    return df

result = retrieve_data(18, 1, ['2019-01-01', '2019-01-15'])

print(result)