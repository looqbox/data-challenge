import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from db_connection import engine


def get_movies():
    query = """
        SELECT
            Title,
            Genre,
            Rating,
            Metascore
        FROM `looqbox-challenge`.IMDB_movies
        WHERE Genre IS NOT NULL
          AND Metascore IS NOT NULL;
    """
    return pd.read_sql(query, engine)


def expand_genres(df):
    df["Genre"] = df["Genre"].str.split(",")
    df = df.explode("Genre")
    df["Genre"] = df["Genre"].str.strip()
    return df


def calculate_correlation_by_genre(df):
    return (
        df.groupby("Genre")
        .filter(lambda x: len(x) >= 20)
        .groupby("Genre")
        .apply(lambda x: x["Rating"].corr(x["Metascore"] / 10))
        .reset_index()
        .rename(columns={0: "Correlation"})
        .sort_values("Correlation", ascending=False)
    )


def plot_correlation_by_genre(df_corr):
    looqbox_cmap = LinearSegmentedColormap.from_list(
        "looqbox", ["#B0B0B0", "#3DBE6E"]
    )

    n = len(df_corr)
    colors = [looqbox_cmap(i / (n - 1)) for i in range(n)]
    colors = colors[::-1]

    fig, ax = plt.subplots(figsize=(11, 7))

    bars = ax.barh(
        df_corr["Genre"],
        df_corr["Correlation"],
        color=colors,
        edgecolor="white",
        linewidth=0.5,
        left=0
    )

    for bar, val in zip(bars, df_corr["Correlation"]):
        ax.text(
            bar.get_width() + 0.005,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.2f}",
            va="center",
            fontsize=9,
            color="#444444"
        )
    avg = df_corr["Correlation"].mean()
    ax.axvline(
        avg,
        color="#e74c3c",
        linestyle="--",
        linewidth=1.5,
        label=f"Overall Average: {avg:.2f}"
    )

    ax.set_title(
        "Audience vs Critics Correlation by Genre",
        fontsize=14, fontweight="bold", pad=15
    )
    ax.set_xlabel("Correlation (Rating vs Metascore)", fontsize=11)
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

    corr_by_genre = calculate_correlation_by_genre(movies)

    print(corr_by_genre.to_string(index=False))

    plot_correlation_by_genre(corr_by_genre)


if __name__ == "__main__":
    main()