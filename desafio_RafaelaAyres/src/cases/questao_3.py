# 3) Criando sua própria visualização
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.conexao_db import get_engine

engine = get_engine()

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#= CONSULTAS #=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

# O top 10 dos filmes mais bem avaliados do IMDB

Consulta_1 = """ 
SELECT Title AS 'Filme', Genre AS 'Gênero', Year as 'Ano de lançamento', Votes as 'Votos'
FROM IMDB_movies 
ORDER BY Votos DESC
LIMIT 10;
"""

# Os gêneros dos filmes que tem maior receita em bilheteria no ano de 2016

consulta_2 = """ 
SELECT Genre AS 'Gênero', SUM(RevenueMillions) as 'Receita Total(USD Milhões)'
FROM IMDB_movies
WHERE year = 2016
GROUP BY Genre
ORDER BY SUM(RevenueMillions) DESC 
LIMIT 8;
"""

df_filmes_avaliados = pd.read_sql(Consulta_1, engine)

df_generos_maior_receita = pd.read_sql(consulta_2, engine)

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#= GERAÇÃO DE GRÁFICOS #=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

# O top 10 dos filmes mais bem avaliados do IMDB
df_filmes_avaliados['Votos_Milhoes'] = df_filmes_avaliados['Votos'] / 1000000.0
plt.figure(figsize=(10, 6))
sns.barplot(x='Votos_Milhoes', y='Filme', data=df_filmes_avaliados, color='royalblue')

plt.title('TOP 10 Filmes com maior engajamento no IMDB', fontsize=14, pad=15)
plt.xlabel('Votos (Em Milhões)', fontsize=12,  labelpad=10) 
plt.ylabel('Filme', fontsize=12)
plt.savefig('output/top_10_filmes.png', bbox_inches='tight')
plt.close()


# Os gêneros dos filmes que tem maior receita em bilheteria no ano de 2016
plt.figure(figsize=(10, 6))
sns.barplot(x='Receita Total(USD Milhões)', y='Gênero', data=df_generos_maior_receita, color='royalblue')
plt.title('Os gêneros com maior receita em 2016', fontsize=12)
plt.xlabel('Receita Total(USD Milhões)', fontsize=12, labelpad=10) 
plt.ylabel('Gênero', fontsize=12)
plt.savefig('output/generos_maior_receita.png', bbox_inches='tight')
plt.close()

# Ambos gráficos foram salvos na pasta output do projeto.

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#= RESULTADOS #=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

print("Questão 1:")
print(df_filmes_avaliados)

print("Questão 2:")
print(df_generos_maior_receita)