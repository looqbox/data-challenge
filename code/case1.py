# %% 
import pandas as pd
import mysql.connector
from mysql.connector import Error
from datetime import datetime
# %%
#função para receber a entrada via teclado do codigo do produto e fazer com que ele seja inteiro
def insert_prod_cod():
    try:
        prod_code = int(input("Digite o codigo do produto que voce irá procurar (apenas numero sem virgulas ou caracteres):"))
    except ValueError as err:
        print("Você precisa inserir um numero inteiro ")
    else:
        if(prod_code > 0):
            return(prod_code)
        print("Não Existe codigo de produto negativo")
    return(insert_prod_cod())


# %%

#função para receber codigo da loja via teclado e garantir que seja inteiro
def insert_store_cod():
    try:
        store_code = int(input("Digite o codigo do Loja que voce irá procurar (apenas numero sem virgulas ou caracteres):"))
    except ValueError as err:
        print("Você precisa inserir um numero inteiro ")
    else:
        if(store_code > 0):
            return(store_code)
        print("Não Existe codigo de produto negativo")
    return(insert_store_cod())

# %%

#função para receber as datas e garantir que estejam no padrao, estejam dentro do range e tambem que 
#os valores de inicio seja menor que a de fim 
def insert_date():
    try:
        date_init = datetime.strptime(input("Digite a data Inicial de pesquisa (YYYY-MM-DD) a data precisa ser entre '2019-01-01', '2019-01-31':"), "%Y-%m-%d")
        date_end = datetime.strptime(input("Digite a data Final de pesquisa (YYYY-MM-DD) a data precisa ser entre '2019-01-01', '2019-01-31':"), "%Y-%m-%d")
        date_range_init = datetime.strptime("2019-01-01","%Y-%m-%d")
        date_range_end = datetime.strptime("2019-12-31","%Y-%m-%d")

    except ValueError as err:
        print("A data esta em formato errado ")
    else:
        if(date_init >= date_end):
            print("Data inicial maior que data final!")
        else:
            if(date_range_init <= date_init <= date_range_end and date_range_init <= date_end <= date_range_end ):
                return([date_init, date_end])
            print(" A data nao esta entre os periodos de '2019-01-01', '2019-12-31'")
    return(insert_date())
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

def sql_table(prod_code, store_code, date):
    connection = connect()
    if connection.is_connected():
        print("Conectado ao banco")
        cursor = connection.cursor()
        cursor.execute("SELECT * " \
        "FROM data_product_sales ;")
        colunas = [coluna[0] for coluna in cursor.description]
        dados = cursor.fetchall()
        data_products_sale =  pd.DataFrame(dados, columns=colunas)

        #Conversão do tipo das colunas para fazer os filtros
        data_products_sale['DATE'] = pd.to_datetime(data_products_sale['DATE'])
        data_products_sale['STORE_CODE'] = data_products_sale['STORE_CODE'].astype(int)
        data_products_sale['PRODUCT_CODE'] = data_products_sale['PRODUCT_CODE'].astype(int)

        #aplicação de filtros nos DFs baseados na entrada
        data_products_sale = data_products_sale[data_products_sale['DATE'].between(*date)]
        data_products_sale = data_products_sale[data_products_sale['STORE_CODE'] == store_code]
        data_products_sale = data_products_sale[data_products_sale['PRODUCT_CODE'] == prod_code]
        cursor.close()
        return(data_products_sale)
# %%
df1 = sql_table(insert_prod_cod(), insert_store_cod(), insert_date())
# %%
print(df1)


# %%
