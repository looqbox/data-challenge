# %% 
import pandas as pd
import mysql.connector
from mysql.connector import Error
from datetime import datetime
# %%

def connect():
    try:
        connection = mysql.connector.connect(
            host="35.199.115.174",
            user="looqbox-challenge",
            password="looq-challenge",
            database="looqbox-challenge"
            )
        return connection

    except Error as e:
        return print(f"Erro ao conectar com o banco: {e}")
# %%
def sales_bytime():
    connection = connect()
    if connection.is_connected():
        print("Conectado ao banco")
        cursor = connection.cursor()
        cursor.execute("SELECT STORE_CODE, STORE_NAME, START_DATE, END_DATE, BUSINESS_NAME, BUSINESS_CODE " \
        "FROM data_store_cad;")
        colunas = [coluna[0] for coluna in cursor.description]
        dados = cursor.fetchall()
        df_data_store =  pd.DataFrame(dados, columns=colunas)

        cursor.execute("SELECT STORE_CODE, DATE, SALES_VALUE, SALES_QTY " \
        "FROM data_store_sales WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31';")
        colunas = [coluna[0] for coluna in cursor.description]
        dados = cursor.fetchall()
        data_store_sales =  pd.DataFrame(dados, columns=colunas)
        cursor.close()

        #junção das tabelas com informações de vendas por loja e nome da loja para criar a tabela agrupada
        df_sales = df_data_store.merge(data_store_sales, on='STORE_CODE')
        #conversão de tipo das colunas
        df_sales['DATE'] = pd.to_datetime(df_sales['DATE'])
        #Filtros 
        df_sales = df_sales[df_sales['DATE'].between('2019-10-01','2019-12-31')]
        #Agrupamento e soma dos valores baseados no nome da loja e no nome do negocio
        df_sales = df_sales[['STORE_NAME','BUSINESS_NAME','SALES_VALUE']].groupby(["STORE_NAME","BUSINESS_NAME"]).sum().sort_values('STORE_NAME')
        return(df_sales)

# %%

print(sales_bytime())
# %%
