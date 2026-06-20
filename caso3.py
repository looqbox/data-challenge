"""
Visualizacoes com IMDB_movies
Autora: Gabriella Pacheco
"""

import pandas as pd
import matplotlib.pyplot as plt
from mysql_conexao import executa_query


def carrega_dados() -> pd.DataFrame:
    return executa_query("SELECT * FROM IMDB_movies")


def prepara_generos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Genre"] = df["Genre"].str.split(",")
    return df.explode("Genre").assign(Genre=lambda x: x["Genre"].str.strip())


def grafico_nota_por_genero(df: pd.DataFrame, ax: plt.Axes):
    df_generos = prepara_generos(df)
    media = (
        df_generos.groupby("Genre")["Rating"]
        .mean()
        .sort_values()
    )

    ax.barh(media.index, media.values, color="#00b6af")
    ax.set_title("Nota Media por Genero", fontsize=13, fontweight="bold")
    ax.set_xlabel("Nota media (IMDb)")
    ax.axvline(media.mean(), color="red", linestyle="--", linewidth=1, label="Media geral")
    ax.legend()


def grafico_receita_vs_nota(df: pd.DataFrame, ax: plt.Axes):
    df_limpo = df.dropna(subset=["RevenueMillions"])

    ax.scatter(df_limpo["Rating"], df_limpo["RevenueMillions"], alpha=0.6, color="#0075b4")
    ax.set_title("Receita x Nota IMDB", fontsize=13, fontweight="bold")
    ax.set_xlabel("Nota (IMDb)")
    ax.set_ylabel("Receita (milhoes USD)")


def main():
    df = carrega_dados()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Analise IMDB Movies", fontsize=15, fontweight="bold")

    grafico_nota_por_genero(df, ax1)
    grafico_receita_vs_nota(df, ax2)

    plt.tight_layout()
    plt.savefig("caso3_imdb.png", dpi=150, bbox_inches="tight")
    print("Grafico salvo: caso3_imdb.png")


if __name__ == "__main__":
    main()