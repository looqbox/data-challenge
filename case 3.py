import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

sns.set_theme(style="whitegrid", font_scale=1.05)

def _get_engine():
    host = os.environ["DB_HOST"]
    port = os.environ.get("DB_PORT", "3306")
    user = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]
    database = os.environ["DB_NAME"]
    url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    return create_engine(url)


engine = _get_engine()
df = pd.read_sql("SELECT * FROM IMDB_movies", engine)

df["MainGenre"] = df["Genre"].str.split(",").str[0]

# Gráfico 1
plt.figure(figsize=(13, 7.5))
palette = sns.color_palette("tab20", n_colors=df["MainGenre"].nunique())
ax = sns.scatterplot(
    data=df, x="Rating", y="RevenueMillions", hue="MainGenre",
    palette=palette, s=70, alpha=0.75, edgecolor="white", linewidth=0.4,
)
ax.set_xlabel("Rating", fontsize=12)
ax.set_ylabel("Receita (milhões $)", fontsize=12)
ax.set_title("Rating vs Receita por Gênero", fontsize=15, fontweight="bold", pad=15)
sns.despine()
ax.legend(
    bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8.5,
    frameon=False, title="Gênero", title_fontsize=9,
)
plt.tight_layout()
plt.savefig("imdb_rating_vs_revenue.png", dpi=150, bbox_inches="tight")
plt.show()

# Gráfico 2
avg_rating = (
    df.groupby("MainGenre", as_index=False)["Rating"]
    .mean()
    .sort_values("Rating", ascending=False)
)

plt.figure(figsize=(12, 6.5))
colors = sns.color_palette("crest", n_colors=len(avg_rating))
ax = sns.barplot(
    data=avg_rating, x="MainGenre", y="Rating",
    palette=colors, edgecolor="black", linewidth=0.6,
)
for i, v in enumerate(avg_rating["Rating"]):
    ax.text(i, v + 0.05, f"{v:.1f}", ha="center", fontsize=9, fontweight="bold")

ax.set_xlabel("Gênero", fontsize=12)
ax.set_ylabel("Rating médio", fontsize=12)
ax.set_title("Rating Médio por Gênero", fontsize=15, fontweight="bold", pad=15)
ax.set_ylim(0, avg_rating["Rating"].max() + 0.8)
plt.xticks(rotation=40, ha="right")
sns.despine()
plt.tight_layout()
plt.savefig("imdb_avg_rating_by_genre.png", dpi=150, bbox_inches="tight")
plt.show()