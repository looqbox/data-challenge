"""
Desafio 3: Building your own visualization

Para este desafio, optei por uma abordagem simples e limpa, focando no 
faturamento dos filmes através de um gráfico de barras horizontais. 
Mesmo sendo uma visualização direta, ela oferece uma informação valiosa e 
muito interessante de se analisar, permitindo uma comparação comercial 
imediata dos grandes sucessos do cinema.
"""

import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

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

# Gera o DataFrame
query = """
    SELECT Title, RevenueMillions
    FROM IMDB_movies
    ORDER BY RevenueMillions DESC
    LIMIT 10;
    """
df = pd.read_sql(query, engine)

# Define o tamanho da tela
plt.figure(figsize=(10, 6))

# 2. Desenha as barras horizontais
df_invertido = df.iloc[::-1]
barras = plt.barh(df_invertido["Title"], df_invertido["RevenueMillions"], color="skyblue")

# Adiciona os valores na ponta de cada barra
plt.bar_label(barras, padding=3)


# Adiciona as labels
plt.title("Top 10 Filmes com Maior Faturamento no IMDB")
plt.xlabel("Faturamento (em Milhões)")
plt.ylabel("Filmes")

# Ajusta os espaçamentos automáticos para o nome dos filmes não sumir da tela
plt.tight_layout()

# Abre a janela
plt.show()