from dotenv import load_dotenv
import os
import mysql.connector
import pandas as pd
import plotly.express as px
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


def manual_query(conexao, query):
    if conexao is None:
        raise ConnectionError("Sem conexão ativa!")

    cursor = conexao.cursor()

    cursor.execute(query)

    result = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]

    return pd.DataFrame(result, columns=columns)

query = """
select * from IMDB_movies
"""
df_query = manual_query(conexao, query)
#print(f'Colunas: {df_query.columns.tolist()}')
#print(df_query)

df_sorted = df_query.sort_values("RevenueMillions", ascending=False)

qnt_filmes = 35

top_movies = df_sorted.head(qnt_filmes)

fig = px.bar(
    top_movies,
    x='RevenueMillions',
    y='Title',
    orientation='h',
    color_continuous_scale=[
        [0.0, '#5B8FF9'],
        [1.0, '#7DAAFF']
    ],
    hover_data={
        'Votes': True,
        'Director': True,
        'Year': True,
        'RevenueMillions': ':.2f',
        'Metascore': True
    },
    labels={
        'RevenueMillions': 'Receita (Milhões USD)',
        'Title': 'Filme',
        'Metascore': 'Metascore',
        'Votes': 'Votos',
        'Director': 'Diretor',
        'Year': 'Ano'
    },
    title=f'Top {qnt_filmes} Filmes por Receita'
)

fig.update_layout(
    yaxis={'categoryorder': 'total ascending'}
)

nome_arquivo = 'grafico_filmes.html'
fig.write_html(nome_arquivo)
print("Gráfico salvo como:",nome_arquivo)