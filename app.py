import streamlit as st
import pandas as pd
import pymysql
import matplotlib.pyplot as plt

# ---------------------------
# CONEXÃO COM BANCO
# ---------------------------
def get_connection():
    return pymysql.connect(
        host="35.199.115.174",
        user="looqbox-challenge",
        password="looq-challenge",
        database="looqbox-challenge",
        port=3306,
        charset="utf8mb4"
    )

def run_query(query):
    conn = get_connection()
    try:
        return pd.read_sql(query, conn)
    finally:
        conn.close()

# ---------------------------
# CONFIG STREAMLIT
# ---------------------------
st.set_page_config(page_title="Looqbox Challenge", layout="wide")
st.title("Looqbox Data Explorer")

menu = st.sidebar.selectbox(
    "Escolha uma análise",
    [
        "Explorar schema",
        "Produtos mais caros",
        "Seções por departamento",
        "Vendas Q1 2019",
        "IMDB Analysis"
    ]
)

# ---------------------------
# 1. SCHEMA
# ---------------------------
if menu == "Explorar schema":
    st.subheader("Tabelas disponíveis no banco")

    df = run_query("SHOW TABLES")
    st.dataframe(df)

# ---------------------------
# 2. PRODUTOS MAIS CAROS
# ---------------------------
elif menu == "Produtos mais caros":
    st.subheader("Top 10 produtos mais caros")

    query = """
    SELECT *
    FROM data_product
    ORDER BY PRODUCT_VAL DESC
    LIMIT 10
    """

    df = run_query(query)
    st.dataframe(df)

# ---------------------------
# 3. SEÇÕES POR DEPARTAMENTO
# ---------------------------
elif menu == "Seções por departamento":
    st.subheader("Seções de BEBIDAS e PADARIA")

    query = """
    SELECT DISTINCT DEP_NAME, SECTION_NAME
    FROM data_product
    WHERE DEP_NAME IN ('BEBIDAS', 'PADARIA')
    """

    df = run_query(query)
    st.dataframe(df)

# ---------------------------
# 4. VENDAS Q1 2019
# ---------------------------
elif menu == "Vendas Q1 2019":
    st.subheader("Total de vendas por Business Area (Q1 2019)")

    query = """
    SELECT
        sc.BUSINESS_NAME,
        SUM(ps.SALES_VALUE) AS TOTAL_SALES
    FROM data_product_sales ps
    JOIN data_store_cad sc
        ON ps.STORE_CODE = sc.STORE_CODE
    WHERE ps.DATE BETWEEN '2019-01-01' AND '2019-03-31'
    GROUP BY sc.BUSINESS_NAME
    ORDER BY TOTAL_SALES DESC
    """

    df = run_query(query)
    st.dataframe(df)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df["BUSINESS_NAME"], df["TOTAL_SALES"])
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# ---------------------------
# 5. IMDB (CORRIGIDO E LEGÍVEL)
# ---------------------------
elif menu == "IMDB Analysis":
    st.subheader("IMDb - Nota média por gênero")

    query = """
    SELECT Genre, Rating
    FROM IMDB_movies
    WHERE Genre IS NOT NULL AND Rating IS NOT NULL
    """

    df = run_query(query)

    df_grouped = (
        df.groupby("Genre")["Rating"]
        .mean()
        .sort_values(ascending=True)
        .reset_index()
    )

    # evita gráfico poluído
    if len(df_grouped) > 15:
        df_grouped = df_grouped.tail(15)

    st.dataframe(df_grouped)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df_grouped["Genre"], df_grouped["Rating"])

    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Genre")
    ax.set_title("IMDb - Average Rating by Genre")

    plt.tight_layout()
    st.pyplot(fig)