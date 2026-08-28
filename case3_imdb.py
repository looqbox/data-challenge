import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import text
from db import get_engine

engine = get_engine()
df = pd.read_sql(text("SELECT * FROM IMDB_movies"), engine)

# --- Gráfico 1 — Receita média por gênero ---
df1 = df.dropna(subset=["RevenueMillions"])

df1 = df1.assign(Genre=df1["Genre"].str.split(",")).explode("Genre")
df1["Genre"] = df1["Genre"].str.strip()

receita_genero = (
    df1.groupby("Genre")["RevenueMillions"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)
contagem_genero = df1.groupby("Genre").size()

plt.figure(figsize=(10, 6))
plot_genero = receita_genero.sort_values()
ax = plot_genero.plot(kind="barh")
ax.set_axisbelow(True)
ax.grid(axis="x", linestyle="--", alpha=0.7)
rotulos_genero = [
    f"{media:.1f} (n={contagem_genero[genero]})"
    for genero, media in plot_genero.items()
]
ax.bar_label(ax.containers[0], labels=rotulos_genero, padding=3)
plt.xlabel("Receita média (milhões $)")
plt.title("Receita média por gênero (Top 10)")
plt.figtext(0.99, 0.01, "n = quantidade de filmes do gênero", ha="right", fontsize=9, style="italic")
plt.tight_layout()
plt.savefig("case3_receita_por_genero.png", dpi=120)
plt.close()

# --- Gráfico 2 — Rating × Receita (receita média por nota) ---
df2 = df.dropna(subset=["RevenueMillions", "Rating"])
receita_por_nota = df2.groupby("Rating")["RevenueMillions"].mean()
contagem_nota = df2.groupby("Rating").size()

corr_receita = df2["Rating"].corr(df2["RevenueMillions"], method="spearman")

plt.figure(figsize=(9, 6))
ax = receita_por_nota.plot(kind="bar")
ax.set_axisbelow(True)
ax.grid(axis="y", linestyle="--", alpha=0.7)
rotulos_nota = [
    f"{media:.1f}\n(n={contagem_nota[nota]})"
    for nota, media in receita_por_nota.items()
]
ax.bar_label(ax.containers[0], labels=rotulos_nota, padding=3)
plt.xlabel("Rating (nota)")
plt.ylabel("Receita média (milhões $)")
plt.title(
    f"Receita média por nota — filme bem avaliado fatura mais? "
    f"(Spearman ρ={corr_receita:.2f})"
)
plt.xticks(rotation=0)
plt.figtext(0.99, 0.01, "n = quantidade de filmes com aquela nota", ha="right", fontsize=9, style="italic")
plt.tight_layout()
plt.savefig("case3_rating_vs_receita.png", dpi=120)
plt.close()

# --- Gráfico 3 — Público (Rating) × Crítica (Metascore) ---
df3 = df.dropna(subset=["Rating", "Metascore"])
notas = sorted(df3["Rating"].unique())
dados_por_nota = [df3.loc[df3["Rating"] == nota, "Metascore"] for nota in notas]

corr_critica = df3["Rating"].corr(df3["Metascore"], method="spearman")

plt.figure(figsize=(9, 6))
ax = plt.gca()
ax.set_axisbelow(True)
ax.grid(axis="y", linestyle="--", alpha=0.7)
rotulos_box = [f"{int(nota)}\nn={len(metascores)}" for nota, metascores in zip(notas, dados_por_nota)]
plt.boxplot(dados_por_nota, tick_labels=rotulos_box)
plt.xlabel("Rating (público)")
plt.ylabel("Metascore (crítica)")
plt.title(
    f"Metascore por nota do público — público e crítica concordam? "
    f"(Spearman ρ={corr_critica:.2f})"
)
plt.figtext(0.99, 0.01, "n = quantidade de filmes com aquela nota", ha="right", fontsize=9, style="italic")
plt.tight_layout()
plt.savefig("case3_publico_vs_critica.png", dpi=120)
plt.close()
