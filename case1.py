from dotenv import load_dotenv
import os
import mysql.connector
import pandas as pd
from sales import SalesRepository

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
port = os.getenv("DB_PORT")


try:
    conexao = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )
    print("Conexão bem-sucedida!")
except mysql.connector.Error as err:
    print(f"Erro ao conectar ao banco de dados: {err}")
    conexao = None


sales_repo = SalesRepository(conexao)

df = sales_repo.retrieve_data(
    product_code=18,
    store_code=1,
    start_date='2019-01-01',
    end_date='2019-01-31'
)

print(df)