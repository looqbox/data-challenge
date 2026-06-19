#%%
import pymysql
import pandas as pd
import matplotlib.pyplot as plt

#%%
conn = pymysql.connect(
    host="35.199.115.174",
    user="looqbox-challenge",
    password="looq-challenge"
)

df = pd.read_sql("SELECT * FROM `looqbox-challenge`.IMDB_movies", conn)

conn.close()

#%%
df["main_genre"] = df["Genre"].str.split(",").str[0].str.strip()
df = df.dropna(subset=["Rating", "RevenueMillions"])

#%%
df_genre = df.groupby("main_genre").agg(
    avg_rating=("Rating", "mean"),
    avg_revenue=("RevenueMillions", "mean"),
    total_movies=("Title", "count")
).reset_index().sort_values("avg_revenue", ascending=False)

df_genre2 = df_genre.sort_values("avg_rating", ascending=False)

#%%
#utilizei llm para a modelagem do gráfico entendi os pontos que deveriam ser levado em consideração como o genero, média de lucro por genero e etc porém não tinha ficado claro a forma q deveria ser montado em código
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

ax1.bar(df_genre["main_genre"], df_genre["avg_revenue"])
ax1.set_title("Receita Média por Gênero (US$ milhões)")
ax1.set_ylabel("Receita Média (US$ M)")
ax1.tick_params(axis="x", rotation=45)

ax2.bar(df_genre2["main_genre"], df_genre2["avg_rating"])
ax2.set_title("Rating Médio IMDb por Gênero")
ax2.set_ylabel("Rating Médio")
ax2.tick_params(axis="x", rotation=45)

#%%
#utilizei llm, no meu primeiro teste o gráfico estava retornando em branco na resposta do terminal da extensão do jupyter do vscode a forma encontrada foi salvar como imagem para utilização
plt.tight_layout()
plt.savefig("case3_imdb.png", dpi=150, bbox_inches="tight")
plt.close()
print("grafico salvo!")
