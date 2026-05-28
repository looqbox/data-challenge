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

def retrieve_data(product_code: int, store_code: int, date: list):
    query = f"""
    SELECT * FROM data_product_sales 
    WHERE PRODUCT_CODE = {product_code} 
        AND STORE_CODE = {store_code}
        AND DATE BETWEEN '{date[0]}' AND '{date[1]}' 
    ORDER BY DATE;
    """ 

    dataframe = pd.read_sql(query, engine)
    
    return dataframe

print(retrieve_data(18, 1, ['2019-01-01', '2019-01-31']))