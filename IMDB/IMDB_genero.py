import pandas as pd
import matplotlib.pyplot as plt
from db_connection import engine
from matplotlib.colors import LinearSegmentedColormap

def get_movies():
    query = """
        SELECT
            Title,
            Genre,
            Rating
        FROM `looqbox-challenge`.IMDB_movies
        WHERE Genre IS NOT NULL;
    """
    return pd.read_sql(query, engine)


def expand_genres(df):
    df["Genre"] = df["Genre"].str.split(",")
    df = df.explode("Genre")
    df["Genre"] = df["Genre"].str.strip()
    return df


def calculate_avg_by_genre(df):
    return (
        df.groupby("Genre")
        .agg(
            Avg_Rating=("Rating", "mean"),
            Count=("Title", "count")
        )
        .reset_index()
        .sort_values("Avg_Rating", ascending=False)
    )


def plot_rating_by_genre(df_genre):
    fig, ax = plt.subplots(figsize=(11, 8))

    looqbox_cmap = LinearSegmentedColormap.from_list(
        "looqbox", ["#B0B0B0", "#3DBE6E"]
    )

    n = len(df_genre)
    colors = [looqbox_cmap(i / (n - 1)) for i in range(n)]
    colors = colors[::-1] 

    bars = ax.barh(
        df_genre["Genre"],
        df_genre["Avg_Rating"] - 5,
        color=colors,
        edgecolor="white",
        linewidth=0.5,
        left=5
    )

    for bar, rating, count in zip(bars, df_genre["Avg_Rating"], df_genre["Count"]):
        ax.text(
            bar.get_x() + bar.get_width() + 0.02,
            bar.get_y() + bar.get_height() / 2,
            f"{rating:.2f}  ({count} filmes)",
            va="center",
            fontsize=9,
            color="#444444"
        )

    avg = df_genre["Avg_Rating"].mean()
    ax.axvline(
        avg,
        color="#e74c3c",
        linestyle="--",
        linewidth=1.5,
        label=f"Overall Average: {avg:.2f}"
    )

    ax.set_xlim(5, df_genre["Avg_Rating"].max() + 0.5)
    ax.set_title("Average IMDb Rating by Genre", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Average Rating", fontsize=11)
    ax.set_ylabel("Genre", fontsize=11)
    ax.legend(fontsize=10)
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.show()


def main():
    movies = get_movies()
    movies = expand_genres(movies)

    avg_by_genre = calculate_avg_by_genre(movies)

    print(avg_by_genre.to_string(index=False))

    plot_rating_by_genre(avg_by_genre)


if __name__ == "__main__":
    main()