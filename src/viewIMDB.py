# ANÁLISE DE RECEITA MÉDIA POR GÊNERO

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


def get_connection():
    return mysql.connector.connect(
        host="35.199.115.174",
        user="looqbox-challenge",
        password="looq-challenge",
        database="looqbox-challenge"
    )


conn = get_connection()

df = pd.read_sql("""
    SELECT *
    FROM IMDB_movies
""", conn)

conn.close()


df["RevenueMillions"] = pd.to_numeric(df["RevenueMillions"], errors="coerce")


df["Genre"] = df["Genre"].fillna("Unknown")
df = df.assign(Genre=df["Genre"].str.split(",")).explode("Genre")

# pegando a média de receita por gênero
genre_revenue = df.groupby("Genre")["RevenueMillions"].mean().sort_values()


plt.figure(figsize=(10,6))
plt.barh(genre_revenue.index, genre_revenue.values)
plt.title("Average Revenue by Genre (IMDB Movies)")
plt.xlabel("Revenue (Millions)")
plt.ylabel("Genre")
plt.tight_layout()
plt.show()

