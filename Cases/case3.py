import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://looqbox-challenge:looq-challenge@35.199.115.174:3306/looqbox-challenge"
)

query = """
SELECT
    Title,
    Genre,
    Year,
    Rating
FROM IMDB_movies
WHERE Genre LIKE '%%Horror%%'
  AND Rating IS NOT NULL
  AND Year IS NOT NULL;
"""

df = pd.read_sql(query, engine)

df_year = (
    df
    .groupby("Year", as_index=False)
    .agg(
        avg_rating=("Rating", "mean"),
        movie_count=("Title", "count")
    )
)

df_year["avg_rating"] = df_year["avg_rating"].round(2)

plt.figure(figsize=(11, 6))

plt.plot(df_year["Year"], df_year["avg_rating"], marker="o")

for _, row in df_year.iterrows():
    plt.text(
        row["Year"],
        row["avg_rating"] + 0.03,
        f'mov_qty={row["movie_count"]}',
        ha='center',
        fontsize=9
    )

plt.title("Average IMDb Rating of Horror Movies by Year", fontsize=16)
plt.xlabel("Year")
plt.ylabel("Average IMDb Rating")

plt.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()
plt.savefig("horror_rating_by_year.png", dpi=300, bbox_inches="tight")
plt.show()

print(df_year)