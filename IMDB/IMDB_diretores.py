import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from db_connection import engine


def get_movies():
    query = """
        SELECT
            Director,
            Rating
        FROM `looqbox-challenge`.IMDB_movies
        WHERE Director IS NOT NULL;
    """
    return pd.read_sql(query, engine)


def calculate_top_directors(df, min_movies=3, top_n=15):
    return (
        df.groupby("Director")
        .filter(lambda x: len(x) >= min_movies)
        .groupby("Director")
        .agg(
            Avg_Rating=("Rating", "mean"),
            Count=("Rating", "count")
        )
        .reset_index()
        .sort_values("Avg_Rating", ascending=False)
        .head(top_n)
    )


def plot_top_directors(df_directors):
    looqbox_cmap = LinearSegmentedColormap.from_list(
        "looqbox", ["#B0B0B0", "#3DBE6E"]
    )

    df_directors = df_directors.sort_values("Avg_Rating", ascending=True)

    n = len(df_directors)
    colors = [looqbox_cmap(i / (n - 1)) for i in range(n)]

    fig, ax = plt.subplots(figsize=(11, 7))

    bars = ax.barh(
        df_directors["Director"],
        df_directors["Avg_Rating"] - 5,
        color=colors,
        edgecolor="white",
        linewidth=0.5,
        left=5
    )

    for bar, rating, count in zip(bars, df_directors["Avg_Rating"], df_directors["Count"]):
        ax.text(
            bar.get_x() + bar.get_width() + 0.02,
            bar.get_y() + bar.get_height() / 2,
            f"{rating:.2f}  ({count} filmes)",
            va="center",
            fontsize=9,
            color="#444444"
        )

    avg = df_directors["Avg_Rating"].mean()
    ax.axvline(
        avg,
        color="#e74c3c",
        linestyle="--",
        linewidth=1.5,
        label=f"Group Average: {avg:.2f}"
    )

    ax.set_xlim(5, df_directors["Avg_Rating"].max() + 0.5)
    ax.set_title(
        "Most Consistent Directors by IMDb Rating",
        fontsize=14, fontweight="bold", pad=15
    )
    ax.set_xlabel("Average IMDb Rating", fontsize=11)
    ax.set_ylabel("Director", fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(axis="x", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.show()

def main():
    movies = get_movies()
    top_directors = calculate_top_directors(movies)

    print(top_directors.to_string(index=False))

    plot_top_directors(top_directors)


if __name__ == "__main__":
    main()