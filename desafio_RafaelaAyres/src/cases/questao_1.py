# 1) A equipe de desenvolvimento estava cansada de desenvolver as mesmas consultas de sempre, 
# variando apenas os filtros de acordo com as exigências do chefe.

import pandas as pd
from src.conexao_db import get_engine

engine = get_engine()

def retrieve_data(product_code=None, store_code=None, date=None):

    query = "SELECT * FROM data_product_sales WHERE 1=1"

    if product_code is not None:
        query += f" AND PRODUCT_CODE = {product_code}"

    if store_code is not None:
        query += f" AND STORE_CODE = {store_code}"

    if date is not None:
        query += f" AND DATE BETWEEN '{date[0]}' AND '{date[1]}'"

    df = pd.read_sql(query, engine)

    return df

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#= LISTA DE TESTES #=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

teste_product = retrieve_data(
    product_code=None,
    store_code=7,
    date=None
)

teste_store = retrieve_data(
    product_code=18,
    store_code=None,
    date=None
)

teste_data = retrieve_data(
    product_code=None,
    store_code=None,
    date=['2019-01-01', '2019-01-31']
)

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#= RESULTADOS #=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

print("\nTeste por código de produto:")
print(teste_product)

print("Teste por código de loja:")
print(teste_store)

print("\nTeste por intervalo de datas:")
print(teste_data)