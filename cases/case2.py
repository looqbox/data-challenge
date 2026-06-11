import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from data.load_and_run import load_sql, run_query


def plot_ticket_medio(df_tm):
    """
    Gera gráfico horizontal de Ticket Médio por Loja.
    """

    category_colors = {
        "Atacado": "#2563EB",
        "Farma": "#16A34A",
        "Posto": "#D97706",
        "Proximidade": "#7C3AED",
        "Varejo": "#DC2626",
    }

    df_plot = df_tm.sort_values("TM", ascending=True)

    colors = (
        df_plot["Categoria"]
        .map(category_colors)
        .fillna("#6B7280")
    )

    fig, ax = plt.subplots(figsize=(10, 7))

    bars = ax.barh(
        df_plot["Loja"],
        df_plot["TM"],
        color=colors,
        edgecolor="white",
        height=0.7,
    )

    # Rótulos de valor
    for bar in bars:
        ax.text(
            bar.get_width() + 0.3,
            bar.get_y() + bar.get_height() / 2,
            f"R$ {bar.get_width():.2f}",
            va="center",
            ha="left",
            fontsize=8.5,
            color="#374151",
        )

    # Legenda
    handles = [
        plt.Rectangle(
            (0, 0),
            1,
            1,
            color=color,
            label=category,
        )
        for category, color in category_colors.items()
    ]

    ax.legend(
        handles=handles,
        title="Categoria",
        loc="lower right",
        fontsize=8,
    )

    ax.set_xlabel("Ticket Médio (R$)", fontsize=10)

    ax.set_title(
        "Ticket Médio por Loja — Q4 2019\n(out–dez)",
        fontsize=13,
        fontweight="bold",
        pad=12,
    )

    ax.xaxis.set_major_formatter(
        mticker.FormatStrFormatter("R$ %.0f")
    )

    ax.spines[["top", "right"]].set_visible(False)

    ax.set_xlim(
        0,
        df_plot["TM"].max() * 1.18
    )

    plt.tight_layout()

    plt.savefig(
        "outputs/case2_ticket_medio.png",
        dpi=150,
    )

    plt.show()

    print(
        "\nGráfico salvo em: outputs/case2_ticket_medio.png"
    )


def execute():
    """
    Calcula o Ticket Médio por Loja para o
    4º trimestre de 2019 utilizando as queries
    fornecidas pelo desafio.
    """

    print(
        "\n=== Case 2: Ticket Médio por Loja — Q4 2019 ==="
    )

    # Carrega queries obrigatórias
    sql_stores = load_sql("04_sql_stores.sql")
    sql_sales = load_sql("05_sql_sales.sql")

    # Executa consultas
    df_stores = run_query(sql_stores)
    df_sales = run_query(sql_sales)

    # Converte coluna para datetime
    df_sales["DATE"] = pd.to_datetime(
        df_sales["DATE"]
    )

    # Filtro do período solicitado
    date_start = pd.Timestamp("2019-10-01")
    date_end = pd.Timestamp("2019-12-31")

    df_sales_q4 = df_sales[
        (df_sales["DATE"] >= date_start)
        &
        (df_sales["DATE"] <= date_end)
    ]

    # Agrega vendas por loja
    df_agg = (
        df_sales_q4
        .groupby(
            "STORE_CODE",
            as_index=False
        )
        .agg(
            total_value=(
                "SALES_VALUE",
                "sum"
            ),
            total_qty=(
                "SALES_QTY",
                "sum"
            ),
        )
    )

    # Calcula Ticket Médio
    df_agg["TM"] = (
        df_agg["total_value"]
        /
        df_agg["total_qty"]
    ).round(2)

    # Junta com cadastro de lojas
    df_result = df_stores.merge(
        df_agg,
        on="STORE_CODE",
        how="inner",
    )

    # Formata resultado final
    df_tm = (
        df_result[
            [
                "STORE_NAME",
                "BUSINESS_NAME",
                "TM",
            ]
        ]
        .rename(
            columns={
                "STORE_NAME": "Loja",
                "BUSINESS_NAME": "Categoria",
            }
        )
        .sort_values("Loja")
        .reset_index(drop=True)
    )

    print(df_tm.to_string(index=False))

    # Gera gráfico
    plot_ticket_medio(df_tm)

    return df_tm