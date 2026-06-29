# 1) The Dev Team was tired of developing the same old queries just varying the filters accordingly to their boss demands.
# As a new member of the crew, your mission now is to create a dynamic function in Python, on the most flexible of
# ways, to produce queries and retrieve a dataframe based on three parameters:

# product_code: integer
# store_code: integer
# date: list of ISO-like strings

# Date e.g.
# ['2019-01-01', '2019-01-31']
# It should look like this my_data = retrieve_data(product_code, store_code, date)

# Extra instructions:

# Retrieve all columns from table data_product_sales;
# Imagine people from other teams will also utilize this function!

from dotenv import load_dotenv
import mysql.connector
import pandas as pd
import os

load_dotenv()

# Pesquisei na documentação do mysql disponível no repositório do desafio o template da conexão
def connect_db():
    cnx = mysql.connector.connect(
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        port=os.getenv("PORT"),
        database=os.getenv("DATABASE")
    )

    return cnx

def retrieve_data(product_code: int, store_code: int, date: list) -> pd.DataFrame:
    cnx = connect_db()

    query = '''
    SELECT *
    FROM data_product_sales
    WHERE PRODUCT_CODE = %s
        AND STORE_CODE = %s
        AND DATE BETWEEN %s AND %s
    ORDER BY DATE DESC;
    '''

    data = pd.read_sql(query, params=(product_code, store_code, date[0], date[1]), con=cnx)
    cnx.close()

    return data

# 2) A brand new client sent you two ready-to-go queries. Those are listed below:

# Query 1:
# SELECT
#       STORE_CODE,
#       STORE_NAME,
#       START_DATE,
#       END_DATE,
#       BUSINESS_NAME,
#       BUSINESS_CODE
# FROM data_store_cad

# Query 2:
# SELECT
#         STORE_CODE,
#         DATE,
#         SALES_VALUE,
#         SALES_QTY
# FROM data_store_sales
# WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
# In addition, he gave you this set of instructions:

# Use the queries as they are (do not modify them or create a new one);

# Please filter the period between this given range:
# ['2019-10-01','2019-12-31']

# We are in need of this visualization (click here to see it)! Please, create it with Python

# Loja	Categoria	TM
# Bahia	Atacado	15.39
# Bangkok	Posto	13.67
# Belem	Proximidade	15.37
# ...

def tm_viz():
    cnx = connect_db()

    query1 = '''
    SELECT
        STORE_CODE,
        STORE_NAME,
        START_DATE,
        END_DATE,
        BUSINESS_NAME,
        BUSINESS_CODE
    FROM data_store_cad
    '''

    query2 = '''
    SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
    FROM data_store_sales
    WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
    '''
    
    table_store_cad = pd.read_sql(query1, con=cnx)
    table_store_sales = pd.read_sql(query2, con=cnx)
    cnx.close()

    data = pd.merge(left=table_store_sales, right=table_store_cad, how='left', on='STORE_CODE').groupby(['STORE_NAME', 'BUSINESS_NAME']).agg({
        'SALES_VALUE': 'sum',
        'SALES_QTY': 'sum'
    }).reset_index()

    data['TM'] = (data['SALES_VALUE'] / data['SALES_QTY']).round(2)
    data = data[['STORE_NAME', 'BUSINESS_NAME', 'TM']].rename(columns={'STORE_NAME': 'Loja', 'BUSINESS_NAME': 'Categoria'})

    return data

# 3) Building your own visualization
# Create at least one chart using the table IMDB_movies. The code must be in Python, and you are free to use any
# libraries, data in the table and graphic format. Explain why you chose the visualization (or visualizations) you are
# submitting.

import matplotlib.pyplot as plt
import seaborn as sns

def imdb_viz():
    cnx = connect_db()

    query = '''
    SELECT *
    FROM IMDB_movies
    '''

    data = pd.read_sql(query, con=cnx)
    cnx.close()

    #--------------------------------------------------------
    # Primeira viz
    #--------------------------------------------------------

    # Escolhi essa visualização para mostrar a relação das notas com o tempo dos filmes.
    # É uma forma interessante de mostrar que filmes antigos que tinham maior duração, 
    # tinham notas mais altas, sugerindo que uma maior duração permite um melhor desenvolvimento
    # da história e dos personagens, deixando uma percepção de maior qualidade resultando em maiores notas.

    # Vou utilizar a coluna Rating como a nota padrão porque é o público geral quem consome e traz a 
    # receita do filme, não a crítica (MetaScore)

    rating_mean = data.groupby('Year')['Rating'].mean()
    runtime_mean = data.groupby('Year')['Runtime'].mean()

    # Pesquisei no Gemini como utilizar dois eixos no mesmo gráfico, foi sugerido a estrutura com subplots (ax1 e ax2)
    fig, ax1 = plt.subplots(figsize=(12, 6))
    color = "tab:blue"
    ax1.set_xlabel("Ano")
    ax1.set_ylabel("Nota Média (Rating)", color=color)
    ax1.plot(rating_mean.index, rating_mean.values, color=color, marker="o")

    ax2 = ax1.twinx()
    color = "tab:red"
    ax2.set_ylabel("Duração Média (Minutos)", color=color)
    ax2.plot(runtime_mean.index, runtime_mean.values, color=color, marker="D")

    plt.title("Comparação da Nota Média vs Duração Média dos Filmes ao Longo dos Anos", fontweight="bold")
    plt.savefig("chart1.png", dpi=300, bbox_inches="tight")
    plt.show()

    #--------------------------------------------------------
    # Segunda viz
    #--------------------------------------------------------
    
    # Escolhi essa visualização por ajudar a direcionar qual gênero será escolhido para produzir um filme,
    # ajudando a ver um panorama geral do mercado.

    # Utilizei o Gemini para sugerir formas de separar os gêneros
    genres = data['Genre'].str.get_dummies(",")
    df_final = pd.concat([data, genres], axis=1).drop(columns=["Genre"])

    revenue_by_genre = df_final[genres.columns].multiply(df_final["RevenueMillions"], axis=0).sum().sort_values()

    ax = revenue_by_genre.plot(kind="barh", color="skyblue", figsize=(12, 6))
    ax.bar_label(ax.containers[0], fontsize=10)

    plt.title('Receita por Gênero', fontweight="bold")
    plt.xlabel('Receita (Milhões $)')
    plt.ylabel('Gênero')
    plt.tight_layout()
    plt.savefig("chart2.png", dpi=300, bbox_inches="tight")
    plt.show()
    
if __name__ == "__main__":

    # Case 1
    data = retrieve_data(21, 9, ['2019-01-01', '2019-01-31'])
    print(data)

    # Case 2
    viz = tm_viz()
    print(viz)

    # Case 3
    imdb_viz()