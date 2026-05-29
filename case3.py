import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
from config import DATABASE_URL

tables = ["IMDB_movies", "imdb_movies"]

df = None
last_error = None

try:
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        for table in tables:
            try:
                query = f"SELECT * FROM `{table}`"
                df = pd.read_sql_query(text(query), con=conn)
                print(f"Table used: {table}")
                break
            except Exception as error:
                last_error = error

except Exception as error:
    last_error = error

if df is None:
    raise Exception(f"Could not load IMDB_movies table. Last error: {last_error}")

df.columns = df.columns.str.strip()

df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df["RevenueMillions"] = pd.to_numeric(df["RevenueMillions"], errors="coerce")
df["Votes"] = pd.to_numeric(df["Votes"], errors="coerce")
df["Runtime"] = pd.to_numeric(df["Runtime"], errors="coerce")
df["Metascore"] = pd.to_numeric(df["Metascore"], errors="coerce")

print(df.head())
print(df.info())

genre_df = df[["Genre", "Rating"]].dropna().copy()

genre_df["Genre"] = genre_df["Genre"].astype(str).str.split(",")
genre_df = genre_df.explode("Genre")
genre_df["Genre"] = genre_df["Genre"].str.strip()

genre_rating = (
    genre_df
    .groupby("Genre", as_index=False)
    .agg(
        average_rating=("Rating", "mean"),
        movies_count=("Rating", "count")
    )
)

genre_rating = genre_rating[genre_rating["movies_count"] >= 5]

genre_rating = (
    genre_rating
    .sort_values("average_rating", ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))
plt.bar(genre_rating["Genre"], genre_rating["average_rating"])
plt.title("Top 10 Genres by Average Rating")
plt.xlabel("Genre")
plt.ylabel("Average Rating")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("01_top_10_genres_by_average_rating.png", dpi=150)
plt.show()

rating_data = df["Rating"].dropna()

plt.figure(figsize=(10, 6))
plt.hist(rating_data, bins=10)
plt.title("Movie Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Number of Movies")
plt.tight_layout()
plt.savefig("02_movie_rating_distribution.png", dpi=150)
plt.show()

revenue_rating = df[["Rating", "RevenueMillions"]].dropna().copy()
revenue_rating = revenue_rating[revenue_rating["RevenueMillions"] > 0]

plt.figure(figsize=(10, 6))
plt.scatter(revenue_rating["Rating"], revenue_rating["RevenueMillions"], alpha=0.6)
plt.title("Rating vs Revenue")
plt.xlabel("Rating")
plt.ylabel("Revenue Millions")
plt.tight_layout()
plt.savefig("03_rating_vs_revenue.png", dpi=150)
plt.show()

print("Charts created successfully.")
print("Files saved:")
print("01_top_10_genres_by_average_rating.png")
print("02_movie_rating_distribution.png")
print("03_rating_vs_revenue.png")
