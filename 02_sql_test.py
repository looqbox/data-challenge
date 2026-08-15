# -*- coding: utf-8 -*-
"""
ETAPA 3 - SQL TEST (3 perguntas do desafio Looqbox)
Schema real descoberto na etapa anterior: `looqbox-challenge` (com hifen).

Q1) 10 produtos mais caros da empresa
Q2) Quais secoes existem nos departamentos 'BEBIDAS' e 'PADARIA'
Q3) Venda total de produtos (em $) por Business Area no 1o trimestre de 2019

Antes das respostas, o script roda um DIAGNOSTICO, porque o mapeamento do schema
mostrou uma armadilha: data_product_sales.STORE_CODE eh varchar(255) e
data_store_cad.STORE_CODE eh int. Juntar as duas sem tratar o tipo pode
descartar linhas silenciosamente.
"""
import os, json, traceback
from urllib.parse import quote_plus
import pandas as pd
from sqlalchemy import create_engine, text

PASTA = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(PASTA, "saida")
os.makedirs(SAIDA, exist_ok=True)

USER, PWD = "looqbox-challenge", "looq-challenge"
HOST, DB = "35.199.115.174", "looqbox-challenge"
ENGINE = create_engine(
    f"mysql+pymysql://{quote_plus(USER)}:{quote_plus(PWD)}@{HOST}/{quote_plus(DB)}?charset=utf8mb4",
    pool_pre_ping=True,
)

linhas = []
def log(msg=""):
    print(msg)
    linhas.append(str(msg))

def roda(titulo, sql, arquivo=None):
    log("\n" + "=" * 78)
    log(titulo)
    log("=" * 78)
    log("SQL:")
    log(sql.strip())
    df = pd.read_sql(text(sql), ENGINE)
    log("\nRESULTADO (%d linhas):" % len(df))
    log(df.to_string(index=False))
    if arquivo:
        df.to_csv(os.path.join(SAIDA, arquivo), index=False, encoding="utf-8-sig")
    return df

try:
    # ------------------------------------------------------------------
    # DIAGNOSTICO: os STORE_CODE das duas tabelas conversam entre si?
    # ------------------------------------------------------------------
    log("#" * 78)
    log("DIAGNOSTICO DE CHAVE (feito antes de responder a Q3)")
    log("#" * 78)

    diag = pd.read_sql(text("""
        SELECT
            (SELECT COUNT(DISTINCT STORE_CODE) FROM data_product_sales)                      AS lojas_em_vendas,
            (SELECT COUNT(DISTINCT STORE_CODE) FROM data_store_cad)                          AS lojas_no_cadastro,
            (SELECT COUNT(*) FROM data_product_sales
              WHERE STORE_CODE REGEXP '[^0-9]')                                              AS vendas_com_codigo_nao_numerico
    """), ENGINE)
    log(diag.to_string(index=False))

    orfas = pd.read_sql(text("""
        SELECT DISTINCT s.STORE_CODE
        FROM data_product_sales s
        LEFT JOIN data_store_cad c ON CAST(s.STORE_CODE AS UNSIGNED) = c.STORE_CODE
        WHERE c.STORE_CODE IS NULL
    """), ENGINE)
    log(f"\nLojas que vendem mas nao existem no cadastro: {len(orfas)}")
    if len(orfas):
        log(orfas.to_string(index=False))

    # ------------------------------------------------------------------
    # Q1) Os 10 produtos mais caros da empresa
    # Raciocinio: preco do produto esta em data_product.PRODUCT_VAL.
    # Nao usei data_product_sales aqui porque la o valor eh venda do dia,
    # nao preco unitario de tabela.
    # ------------------------------------------------------------------
    q1 = """
SELECT
    PRODUCT_COD,
    PRODUCT_NAME,
    PRODUCT_VAL,
    DEP_NAME,
    SECTION_NAME
FROM data_product
ORDER BY PRODUCT_VAL DESC
LIMIT 10
"""
    roda("Q1) OS 10 PRODUTOS MAIS CAROS DA EMPRESA", q1, "02_q1_top10_produtos.csv")

    # confere empate na fronteira do top 10 (o 11o tem o mesmo preco do 10o?)
    fronteira = pd.read_sql(text("""
        SELECT PRODUCT_VAL, COUNT(*) AS qtd_produtos
        FROM data_product
        WHERE PRODUCT_VAL >= (
            SELECT MIN(PRODUCT_VAL) FROM (
                SELECT PRODUCT_VAL FROM data_product ORDER BY PRODUCT_VAL DESC LIMIT 10
            ) t
        )
        GROUP BY PRODUCT_VAL
        ORDER BY PRODUCT_VAL DESC
    """), ENGINE)
    log("\nCHECAGEM DE EMPATE NA 10a POSICAO:")
    log(fronteira.to_string(index=False))

    # ------------------------------------------------------------------
    # Q2) Secoes dos departamentos BEBIDAS e PADARIA
    # DISTINCT porque a granularidade da tabela eh produto, nao secao.
    # ------------------------------------------------------------------
    q2 = """
SELECT DISTINCT
    DEP_COD,
    DEP_NAME,
    SECTION_COD,
    SECTION_NAME
FROM data_product
WHERE DEP_NAME IN ('BEBIDAS', 'PADARIA')
ORDER BY DEP_NAME, SECTION_NAME
"""
    roda("Q2) SECOES DOS DEPARTAMENTOS 'BEBIDAS' E 'PADARIA'", q2, "02_q2_secoes.csv")

    # quantos produtos por secao, so pra dar contexto na resposta
    q2b = """
SELECT
    DEP_NAME,
    SECTION_NAME,
    COUNT(*) AS QTD_PRODUTOS
FROM data_product
WHERE DEP_NAME IN ('BEBIDAS', 'PADARIA')
GROUP BY DEP_NAME, SECTION_NAME
ORDER BY DEP_NAME, QTD_PRODUTOS DESC
"""
    roda("Q2b) QUANTIDADE DE PRODUTOS POR SECAO (contexto extra)", q2b, "02_q2b_produtos_por_secao.csv")

    # ------------------------------------------------------------------
    # Q3) Venda total de produtos por Business Area no 1o trimestre de 2019
    # Uso data_product_sales (venda DE PRODUTO, como a pergunta pede) e nao
    # data_store_sales (venda agregada da loja, que inclui o que nao eh produto).
    # O CAST resolve o varchar x int do STORE_CODE.
    # ------------------------------------------------------------------
    q3 = """
SELECT
    c.BUSINESS_CODE,
    c.BUSINESS_NAME                       AS BUSINESS_AREA,
    ROUND(SUM(s.SALES_VALUE), 2)          AS VENDA_TOTAL_1T2019,
    SUM(s.SALES_QTY)                      AS QTD_TOTAL_1T2019,
    COUNT(DISTINCT s.STORE_CODE)          AS QTD_LOJAS
FROM data_product_sales s
INNER JOIN data_store_cad c
        ON CAST(s.STORE_CODE AS UNSIGNED) = c.STORE_CODE
WHERE s.DATE BETWEEN '2019-01-01' AND '2019-03-31'
GROUP BY c.BUSINESS_CODE, c.BUSINESS_NAME
ORDER BY VENDA_TOTAL_1T2019 DESC
"""
    df3 = roda("Q3) VENDA TOTAL DE PRODUTOS POR BUSINESS AREA - 1o TRIMESTRE DE 2019", q3, "02_q3_business_area.csv")

    # controle: o total do trimestre sem quebrar por area tem que bater com a soma acima
    total = pd.read_sql(text("""
        SELECT ROUND(SUM(SALES_VALUE), 2) AS TOTAL_GERAL_1T2019
        FROM data_product_sales
        WHERE DATE BETWEEN '2019-01-01' AND '2019-03-31'
    """), ENGINE)
    log("\nCONTROLE - total geral do trimestre sem join:")
    log(total.to_string(index=False))
    log(f"Soma das areas: {df3['VENDA_TOTAL_1T2019'].sum():,.2f}")
    log("As duas linhas acima precisam bater. Se nao baterem, o join perdeu venda.")

    log("\n[ok] SQL TEST CONCLUIDO")

except Exception:
    log("\n[XX] ERRO:")
    log(traceback.format_exc())

with open(os.path.join(SAIDA, "02_sql_test.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(linhas))

print("\n>>> Saida em: " + SAIDA)
