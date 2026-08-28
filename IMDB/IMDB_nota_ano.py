import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from db_connection import engine


def get_movies():
    query = """
        SELECT
            Title,
            Year,
            Rating
        FROM `looqbox-challenge`.IMDB_movies
        WHERE Year IS NOT NULL;
    """
    return pd.read_sql(query, engine)


def plot_rating_by_year(df):
    avg_by_year = (
        df.groupby("Year")["Rating"]
        .mean()
        .reset_index()
    )

    looqbox_cmap = LinearSegmentedColormap.from_list(
        "looqbox", ["#B0B0B0", "#3DBE6E"]
    )

    ratings = avg_by_year["Rating"]
    norm = (ratings - ratings.min()) / (ratings.max() - ratings.min())
    colors = [looqbox_cmap(v) for v in norm]

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        avg_by_year["Year"],
        avg_by_year["Rating"],
        color="#B0B0B0",
        linewidth=2,
        zorder=1
    )

    for x, y, c in zip(avg_by_year["Year"], avg_by_year["Rating"], colors):
        ax.scatter(x, y, color=c, s=80, zorder=2, edgecolors="white", linewidths=0.8)
        ax.text(x, y + 0.015, f"{y:.2f}", ha="center", fontsize=8, color="#444444")

    avg = ratings.mean()
    ax.axhline(
        avg,
        color="#e74c3c",
        linestyle="--",
        linewidth=1.5,
        label=f"Overall Average: {avg:.2f}"
    )

    ax.set_title("Average IMDb Rating by Year", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Year", fontsize=11)
    ax.set_ylabel("Average Rating", fontsize=11)
    ax.set_ylim(ratings.min() - 0.1, ratings.max() + 0.1)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.show()


def main():
    movies = get_movies()
    plot_rating_by_year(movies)


if __name__ == "__main__":
    main()