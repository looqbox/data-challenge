# %%

import pandas as pd
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# %%
#Conexão com banco de dados
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

# Desafio 1
def top_10_expensive():
    connection = connect()
    if connection.is_connected():
        print("Conectado ao banco")
        cursor = connection.cursor()
        #Query para pegar os 10 produtos mais caros
        cursor.execute("SELECT PRODUCT_NAME, PRODUCT_VAL  " \
        "FROM data_product ORDER BY PRODUCT_VAL DESC LIMIT 10;")
        colunas = [coluna[0] for coluna in cursor.description]
        dados = cursor.fetchall()
        df_produtos_mais_caros =  pd.DataFrame(dados, columns=colunas)
        print(df_produtos_mais_caros)
        cursor.close()

    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("\nConexão encerrada!")
# %%
top_10_expensive()

# %%
# Desafio 2
def sections_departaments():
    connection = connect()
    if connection.is_connected():
        print("Conectado ao banco")
        cursor = connection.cursor()
        #Query para mostrar quais seções tem  nos departamentos de BEBIDAS E PADARIA
        cursor.execute("SELECT DISTINCT SECTION_NAME,DEP_NAME  FROM data_product " \
        "WHERE DEP_NAME IN ('BEBIDAS','PADARIA') ORDER BY DEP_NAME;")
        colunas = [coluna[0] for coluna in cursor.description]
        dados = cursor.fetchall()
        df_section_name =  pd.DataFrame(dados, columns=colunas)
        print(df_section_name)
        cursor.close()

    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("\nConexão encerrada!")


# %%
sections_departaments()
#%%
#Desafio 3
def total_sales_BA_quarter():
    connection = connect()
    if connection.is_connected():
        print("Conectado ao banco")
        cursor = connection.cursor()
        #Query para mostrar o total de vendas por area de negocio no primeiro quarter de 2019
        cursor.execute("SELECT a.BUSINESS_NAME, SUM(b.SALES_VALUE) AS total_sales, SUM(b.SALES_QTY) AS total_qtd " \
        "FROM data_store_cad AS a " \
        "JOIN data_store_sales AS b " \
        "ON a.STORE_CODE = b.STORE_CODE " \
        "WHERE b.DATE BETWEEN '2019-01-31' AND '2019-04-30' " \
        "GROUP BY a.BUSINESS_NAME " \
        "ORDER BY total_sales DESC;")
        colunas = [coluna[0] for coluna in cursor.description]
        dados = cursor.fetchall()
        df_total_vendas =  pd.DataFrame(dados, columns=colunas)
        print(df_total_vendas)
        cursor.close()

    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("\nConexão encerrada!")
total_sales_BA_quarter()