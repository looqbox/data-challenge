"""
Respostas para o SQL Test do desafios.
Autora: Gabriella Pacheco
"""

import matplotlib.pyplot as plt
from mysql_conexao import executa_query


# Top 10 produtos mais caros 

def produtos_mais_caros():
    sql = """
        SELECT
            PRODUCT_NAME,
            PRODUCT_VAL
        FROM data_product
        ORDER BY PRODUCT_VAL DESC
        LIMIT 10
    """
    return executa_query(sql)


def grafico_produtos(df):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.barh(df["PRODUCT_NAME"], df["PRODUCT_VAL"], color="#4C72B0")
    ax.invert_yaxis()
    ax.set_xlabel("Valor (R$)")
    ax.set_title("Top 10 produtos mais caros", fontweight="bold")

    for i, val in enumerate(df["PRODUCT_VAL"]):
        ax.text(val + 0.5, i, f"R$ {val:,.2f}", va="center", fontsize=9)

    plt.tight_layout()
    plt.savefig("grafico_1_produtos.png", dpi=150)
    plt.show()
    print("Gráfico salvo: grafico_1_produtos.png\n")


# Seções dos departamentos BEBIDAS e PADARIA 

def secoes_por_departamento():
    sql = """
        SELECT DISTINCT
            DEP_NAME,
            SECTION_NAME
        FROM data_product
        WHERE DEP_NAME IN ('BEBIDAS', 'PADARIA')
        ORDER BY DEP_NAME, SECTION_NAME
    """
    return executa_query(sql)


def grafico_secoes(df):
    contagem = df.groupby("DEP_NAME")["SECTION_NAME"].count()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    cores = {"BEBIDAS": "#4C72B0", "PADARIA": "#DD8452"}

    for ax, (dep, grupo) in zip(axes, df.groupby("DEP_NAME")):
        secoes = grupo["SECTION_NAME"].tolist()
        ax.barh(secoes, [1] * len(secoes), color=cores.get(dep, "#888"))
        ax.set_xlim(0, 1.5)
        ax.set_xticks([])
        ax.set_title(f"{dep}  ({len(secoes)} seções)", fontweight="bold")
        ax.invert_yaxis()

    plt.suptitle("Secoes por departamento", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig("grafico_2_secoes.png", dpi=150)
    plt.show()
    print("Gráfico salvo: grafico_2_secoes.png\n")


#  Total de vendas por Business Area no Q1 2019 

def vendas_por_business_area():
    sql = """
        SELECT
            sc.BUSINESS_NAME,
            SUM(ss.SALES_VALUE) AS TOTAL_VENDAS
        FROM data_store_sales ss
        JOIN data_store_cad sc ON ss.STORE_CODE = sc.STORE_CODE
        WHERE ss.DATE BETWEEN '2019-01-01' AND '2019-03-31'
        GROUP BY sc.BUSINESS_NAME
        ORDER BY TOTAL_VENDAS DESC
    """
    return executa_query(sql)


def grafico_vendas(df):
    cores = ["#00b6af", "#00a2bd", "#008cbf", "#0075b4", "#435c9c"]
    
    fig, ax = plt.subplots(figsize=(9, 5))

    bars = ax.bar(df["BUSINESS_NAME"], df["TOTAL_VENDAS"], color=cores)
    ax.set_ylabel("Total de Vendas (R$)")
    ax.set_title("Vendas por Business Area Q1 2019", fontweight="bold")
    ax.tick_params(axis="x", rotation=25)

    for bar, val in zip(bars, df["TOTAL_VENDAS"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(df["TOTAL_VENDAS"]) * 0.01,
            f"R$ {val:,.0f}",
            ha="center", va="bottom", fontsize=8
        )

    plt.tight_layout()
    plt.savefig("grafico_3_vendas.png", dpi=150)
    plt.show()
    print("Gráfico salvo: grafico_3_vendas.png\n")


# Execução 

if __name__ == "__main__":

    print("\n Top 10 produtos mais caros")
    df1 = produtos_mais_caros()
    print(df1.to_string(index=False))
    grafico_produtos(df1)

    print("\n Secoess de BEBIDAS e PADARIA")
    df2 = secoes_por_departamento()
    print(df2.to_string(index=False))
    grafico_secoes(df2)

    print("\n Vendas por Business Area Q1 2019 ")
    df3 = vendas_por_business_area()
    print(df3.to_string(index=False))
    grafico_vendas(df3)