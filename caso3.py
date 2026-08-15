import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# Visual mais limpo
sns.set_theme(style="whitegrid")

# Conexão e Extração
engine = create_engine(
    "mysql+pymysql://looqbox-challenge:looq-challenge@35.199.115.174:3306/looqbox-challenge"
)
query_imdb = "SELECT * FROM IMDB_movies"
df_imdb = pd.read_sql(query_imdb, engine)

# print(df_imdb.shape)
# print(df_imdb.columns.tolist())
# print(df_imdb.head())
# print(df_imdb.info())

# Transformação e Cálculo
df_1 = df_imdb[["Title", "Rating", "Votes", "RevenueMillions", "Metascore"]].copy()
correlation_votes = df_1["Votes"].corr(df_1["Rating"])

# Visualização de Dados
plt.figure(figsize=(10, 6)) 

sns.scatterplot(
    data=df_1,
    x="Votes",
    y="Rating",
    alpha=0.5,
    color="#1f77b4",
    edgecolor="w",
    linewidth=0.5
)

# Ajustes de Escala e Rótulos
plt.xscale("log")
plt.xlabel("Volume de Votos (Escala Logarítmica)", fontsize=11, labelpad=10)
plt.ylabel("Avaliação do Público (Rating IMDB)", fontsize=11, labelpad=10)

# Título
plt.title("O Engajamento do Público vs. A Qualidade do Filme\n", fontsize=14, fontweight="bold", loc="left")

# Anotação da Correlação
plt.annotate(
    f"Correlação de Pearson (r): {correlation_votes:.2f}\n(Correlação Positiva Moderada)", 
    xy=(0.02, 0.05), 
    xycoords='axes fraction',
    fontsize=11,
    bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="gray", alpha=0.8)
)

# Removendo as bordas superior e direita
sns.despine()

plt.tight_layout()
plt.show()

# ------ SEGUNDA ANÁLISE: RECEITA MÉDIA POR GÊNERO -----

# Cópia do dataframe e removendo filmes sem dados de receita
df_2 = df_imdb.dropna(subset=['RevenueMillions']).copy()

df_2['Genre_List'] = df_2['Genre'].str.split(',')
df_expl = df_2.explode('Genre_List')

# print(df_expl['Genre_List'].unique())

# Agregação de Dados
df_top_generos = (
    df_expl.groupby('Genre_List')['RevenueMillions']
    .mean()
    .sort_values(ascending=False)
    .head(10) # top10
    .reset_index()
)

# Visualização de Dados
plt.figure(figsize=(10, 6))

barplot = sns.barplot(
    data=df_top_generos, 
    x='RevenueMillions', 
    y='Genre_List', 
    palette='Blues_r' 
)

plt.xlabel("Receita Média (Milhões de USD)", fontsize=11, labelpad=10)
plt.ylabel("Gênero Cinematográfico", fontsize=11, labelpad=10)
plt.title("Top 10 Gêneros Cinematográficos Mais Lucrativos\n", 
          fontsize=14, fontweight="bold", loc="left")

# Adicionando os valores exatos no final de cada barra
for index, value in enumerate(df_top_generos['RevenueMillions']):
    plt.text(value + 2, index, f"${value:.1f}M", va='center', fontsize=10, color='black')

sns.despine(bottom=True)
plt.xticks(visible=False) 

plt.tight_layout()
plt.show()