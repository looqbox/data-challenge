import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from db_connection import engine


def get_movies():
    query = """
        SELECT
            Title,
            Rating,
            Metascore,
            Genre
        FROM `looqbox-challenge`.IMDB_movies
        WHERE Metascore IS NOT NULL;
    """
    return pd.read_sql(query, engine)


def calculate_difference(df):
    df["Rating_scaled"] = df["Rating"] * 10
    df["Difference"] = df["Rating_scaled"] - df["Metascore"]
    return df


def get_looqbox_cmap():
    return LinearSegmentedColormap.from_list(
        "looqbox", ["#B0B0B0", "#3DBE6E"]
    )


def plot_divergence(df):
    top = (
        df.reindex(df["Difference"].abs().sort_values(ascending=False).index)
        .head(20)
        .sort_values("Difference")
    )

    cmap = get_looqbox_cmap()
    norm = (top["Difference"] - top["Difference"].min()) / (
        top["Difference"].max() - top["Difference"].min()
    )
    colors = [cmap(v) for v in norm]

    fig, ax = plt.subplots(figsize=(11, 8))

    bars = ax.barh(
        top["Title"],
        top["Difference"],
        color=colors,
        edgecolor="white",
        linewidth=0.5
    )

    for bar, val in zip(bars, top["Difference"]):
        x = bar.get_width()
        ax.text(
            x + (0.5 if x >= 0 else -0.5),
            bar.get_y() + bar.get_height() / 2,
            f"{val:+.1f}",
            va="center",
            ha="left" if x >= 0 else "right",
            fontsize=9,
            color="#444444"
        )

    ax.axvline(0, color="#444444", linewidth=1)

    ax.text(
        top["Difference"].max() * 0.3, -2,
        "► Público gostou mais",
        color="#3DBE6E", fontsize=10, fontweight="bold"
    )
    ax.text(
        top["Difference"].min() * 0.9, -2,
        "◄ Crítica gostou mais",
        color="#B0B0B0", fontsize=10, fontweight="bold"
    )

    ax.set_title(
        "Audience vs Critics: Who Liked It More?",
        fontsize=14, fontweight="bold", pad=15
    )
    ax.set_xlabel("Difference (Audience Score - Critics Score)", fontsize=11)
    ax.grid(axis="x", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.show()


def main():
    movies = get_movies()
    movies = calculate_difference(movies)

    print("Top 10 Biggest Disagreements:\n")
    print(
        movies.reindex(movies["Difference"].abs().sort_values(ascending=False).index)
        [["Title", "Rating", "Metascore", "Difference"]]
        .head(10)
        .to_string(index=False)
    )

    plot_divergence(movies)


if __name__ == "__main__":
    main()