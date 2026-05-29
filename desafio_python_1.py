# Desafio 1: The Dev Team was tired of developing the same old queries...

import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Carrega as variáveis de ambiente
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Monta a string de conexão
connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Cria o motor de conexão
engine = create_engine(connection_string)

def get_product_sales_dataframe(product_code: int, store_code: int, date: list):
    """
    Retorna um DataFrame da tabela 'data_product_sales' com base nos parâmetros fornecidos.
    
    Parâmetros:
    - product_code (int): Código do produto.
    - store_code (int): Código da loja.
    - date (list): Lista contendo o intervalo de datas [data_inicio, data_fim].
    """

    # Constroi a query
    query = f"""
    SELECT * FROM data_product_sales 
    WHERE PRODUCT_CODE = {product_code} 
        AND STORE_CODE = {store_code}
        AND DATE BETWEEN '{date[0]}' AND '{date[1]}' 
    ORDER BY DATE;
    """ 

    # Executa a query usando a engine fornecida e carrega o resultado já como um dataframe
    df = pd.read_sql(query, engine)
    
    # Retorna o dataframe
    return df
