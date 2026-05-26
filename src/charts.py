from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import seaborn as sns


def plot_top_genres_by_rating(movies, min_movies=10, top_n=10, logo_path="logo.png"):
    ranking_generos = (
        movies.groupby("Genre", as_index=False)
              .agg(
                  nota_media=("Rating", "mean"),
                  qtd_filmes=("Rating", "count")
              )
    )

    ranking_generos = ranking_generos[ranking_generos["qtd_filmes"] >= min_movies]
    ranking_generos = ranking_generos.sort_values("nota_media", ascending=False).head(top_n)

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        data=ranking_generos,
        y="Genre",
        x="nota_media",
        color="#4C78A8",
        ax=ax
    )

    ax.set_title("Top generos por nota media no IMDb", pad=18)
    ax.set_xlabel("Nota media")
    ax.set_ylabel("Genero")

    logo_file = Path(logo_path)
    if logo_file.exists():
        logo = mpimg.imread(logo_file)
        logo_ax = fig.add_axes([0.82, 0.91, 0.14, 0.07], anchor="NE", zorder=10)
        logo_ax.imshow(logo)
        logo_ax.axis("off")

    fig.tight_layout(rect=[0, 0, 1, 0.90])

    return fig
