# %% 
import pandas as pd
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
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

connection = connect()
if connection.is_connected():
    print("Conectado ao banco")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM IMDB_movies;")
    colunas = [coluna[0] for coluna in cursor.description]
    dados = cursor.fetchall()
    df1 =  pd.DataFrame(dados, columns=colunas)
    cursor.close()

# %%

#Fazendo Grafico de quantidade de filmes por ano
df_movies_year = df1.groupby("Year").size().sort_index()
plt.bar(df_movies_year.index, df_movies_year.values )
plt.title ("Número de Filmes por ano")
plt.xlabel("Ano")
plt.ylabel("Num de Filmes")
plt.show()
# %%

#Fazendo grafico de quantidade de filmes por rating com range

#criação de uma coluna separando os ranges por grupos de 0 ate 4, 5 a 8 e 9 a 10
intervalos = [0, 4.9, 8.9, 10.1]
nomes_faixas = ["0 a 4", "5 a 8", "9 e 10 (Ótimo)"]
df1["faixa_rating"] = pd.cut(df1["Rating"], bins=intervalos, labels=nomes_faixas, right=False)

movies_rating = df1.groupby("faixa_rating").size().sort_index()

plt.bar(movies_rating.index, movies_rating.values )
plt.title ("Número de Filmes por faixa de Rating")
plt.xlabel("Faixa de Rating")
plt.ylabel("Num de Filmes")
plt.show()
# %%

##Fazendo grafico de dispersão para verificar o retorno do filme baseado no rating
valores_y = np.arange(0, int(df1['RevenueMillions'].max()) + 100, 100)
plt.yticks(valores_y)
plt.grid(axis="y", linestyle="--", alpha=0.7, color="gray")
plt.scatter(df1['Rating'], df1['RevenueMillions'])
plt.title ("Relação de Rating e Bilheteria")
plt.xlabel("Rating")
plt.ylabel("Retorno Bilheteria")
plt.show()
