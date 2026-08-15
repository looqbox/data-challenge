"""Case 3: compare average IMDB rating across sufficiently represented genres."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import text

from database import create_database_engine


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"
CHART_DIR = PROJECT_ROOT / "outputs" / "charts"
MIN_MOVIES = 30


def build_genre_summary() -> pd.DataFrame:
    engine = create_database_engine()
    with engine.connect() as connection:
        movies = pd.read_sql_query(
            text("SELECT Id, Genre, Rating FROM IMDB_movies WHERE Genre IS NOT NULL AND Rating IS NOT NULL"),
            connection,
        )
    engine.dispose()

    movies["Rating"] = pd.to_numeric(movies["Rating"])
    exploded = movies.assign(Genre=movies["Genre"].str.split(",")).explode("Genre")
    exploded["Genre"] = exploded["Genre"].str.strip()
    summary = (
        exploded.groupby("Genre", as_index=False)
        .agg(Filmes=("Id", "nunique"), Avaliacao_media=("Rating", "mean"))
        .query("Filmes >= @MIN_MOVIES")
        .sort_values("Avaliacao_media", ascending=False)
        .reset_index(drop=True)
    )
    return summary


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    summary = build_genre_summary()
    summary.to_csv(TABLE_DIR / "case_03_rating_by_genre.csv", index=False, float_format="%.2f")

    plot_data = summary.sort_values("Avaliacao_media")
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(plot_data["Genre"], plot_data["Avaliacao_media"], color="#7C3AED")
    ax.set(
        title=f"Avaliação média por gênero — mínimo de {MIN_MOVIES} filmes",
        xlabel="Avaliação média",
        ylabel="",
        xlim=(0, 10),
    )
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "case_03_rating_by_genre.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"Case 3 complete: {len(summary)} represented genres")


if __name__ == "__main__":
    main()
