import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database import get_engine

engine = get_engine()

def plot_rating_distribution():
    query = """
    SELECT
        rating, genre
    FROM IMDB_movies
    WHERE
        rating IS NOT NULL AND genre IS NOT NULL
    """
    df = pd.read_sql(query, engine)

    df['genre'] = df['genre'].astype(str)
    df_exploded = df.assign(genre=df['genre'].str.split(',')).explode('genre')
    df_exploded['genre'] = df_exploded['genre'].str.strip()

    top_genres = df_exploded['genre'].value_counts().nlargest(5).index
    df_filters = df_exploded[df_exploded['genre'].isin(top_genres)]

    df_means = df_filters.groupby('genre')['rating'].mean().reset_index()
    df_means = df_means.sort_values(by='rating', ascending=False)

    plt.figure(figsize=(9, 5))
    sns.set_theme(style="whitegrid")

    sns.barplot(
        data=df_means,
        x='rating',
        y='genre',
        color='steelblue'
    )

    plt.title('Média de Avaliação por Gênero (Top 5)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Média de Avaliação', fontsize=11)
    plt.ylabel('Gênero', fontsize=11)

    plt.tight_layout()
    plt.show()