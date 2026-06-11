import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from data.load_and_run import run_query


def plot_rating_by_decade(df_imdb):
    """
    Gera violin plot com a distribuição das notas IMDB por década.
    """

    fig, ax = plt.subplots(figsize=(14, 6))

    decade_order = sorted(
        df_imdb["Década"].unique()
    )

    sns.violinplot(
        data=df_imdb,
        x="Década",
        y="RATING",
        order=decade_order,
        palette="mako",
        inner="quartile",
        linewidth=0.8,
        ax=ax,
    )

    ax.set_title(
        "Distribuição das Notas IMDB por Década",
        fontsize=13,
        fontweight="bold",
        pad=12,
    )

    ax.set_xlabel(
        "Década de Lançamento",
        fontsize=10,
    )

    ax.set_ylabel(
        "Nota IMDB (0–10)",
        fontsize=10,
    )

    ax.spines[
        ["top", "right"]
    ].set_visible(False)

    plt.xticks(rotation=30)
    plt.tight_layout()

    plt.savefig(
        "outputs/case3_imdb_violinplot.png",
        dpi=150,
    )

    plt.show()

    print(
        "\nGráfico salvo em: outputs/case3_imdb_violinplot.png"
    )


def plot_genre_ranking():
    """
    Gera ranking dos gêneros com maior nota média.
    """

    sql_genre = """
    SELECT
        GENRE,
        ROUND(AVG(RATING), 2) AS Nota_Media,
        COUNT(*) AS Qtd_Filmes
    FROM IMDB_movies
    WHERE GENRE IS NOT NULL
      AND RATING IS NOT NULL
    GROUP BY GENRE
    HAVING COUNT(*) >= 20
    ORDER BY Nota_Media DESC
    LIMIT 10;
    """

    try:

        df_genre = run_query(sql_genre)

        fig, ax = plt.subplots(figsize=(9, 5))

        ax.barh(
            df_genre["GENRE"],
            df_genre["Nota_Media"],
            color=sns.color_palette(
                "mako",
                len(df_genre),
            ),
        )

        ax.set_xlabel(
            "Nota Média IMDB"
        )

        ax.set_title(
            "Top 10 Gêneros por Nota Média (mín. 20 filmes)",
            fontweight="bold",
        )

        ax.spines[
            ["top", "right"]
        ].set_visible(False)

        ax.set_xlim(0, 10)

        plt.tight_layout()

        plt.savefig(
            "outputs/case3_imdb_genre.png",
            dpi=150,
        )

        plt.show()

        print(
            "Gráfico salvo em: outputs/case3_imdb_genre.png"
        )

    except Exception as e:

        print(
            f"Coluna GENRE não disponível ou erro: {e}"
        )


def execute():
    """
    Case 3 - Análise exploratória da base IMDB_movies.
    """

    print(
        "\n=== Case 3: Visualização IMDB ==="
    )

    # Amostra para inspeção das colunas
    df_imdb_sample = run_query(
        "SELECT * FROM IMDB_movies LIMIT 5;"
    )

    print(
        "\n=== Colunas disponíveis em IMDB_movies ==="
    )

    print(df_imdb_sample.dtypes)
    print(df_imdb_sample.head(2))

    print(
        """
Justificativa da visualização:

O violin plot foi escolhido porque permite visualizar
não apenas medidas centrais (média e mediana),
mas também a distribuição completa das notas ao longo
das décadas. Dessa forma é possível identificar
assimetrias, dispersão e concentração das avaliações,
algo que um gráfico de barras de médias não mostraria.
"""
    )

    sql_imdb = """
    SELECT
        YEAR,
        RATING
    FROM IMDB_movies
    WHERE YEAR IS NOT NULL
      AND RATING IS NOT NULL
      AND YEAR >= 1920;
    """

    df_imdb = run_query(sql_imdb)

    df_imdb["YEAR"] = pd.to_numeric(
        df_imdb["YEAR"],
        errors="coerce",
    )

    df_imdb["RATING"] = pd.to_numeric(
        df_imdb["RATING"],
        errors="coerce",
    )

    df_imdb.dropna(inplace=True)

    df_imdb["Década"] = (
        (df_imdb["YEAR"] // 10 * 10)
        .astype(int)
        .astype(str)
        + "s"
    )

    # Gráfico principal
    plot_rating_by_decade(df_imdb)

    # Gráfico complementar
    plot_genre_ranking()

    print(
        "\n✅ Case 3 executado com sucesso."
    )

    return df_imdb