# -*- coding: utf-8 -*-
"""
ETAPA 4 - CASE 1: demonstracao e teste da funcao retrieve_data.
Roda os cenarios que outro time usaria no dia a dia, incluindo os casos de erro,
porque funcao que so foi testada no caminho feliz nao esta testada.
"""
import os, traceback
import pandas as pd
from looqbox_data import retrieve_data

PASTA = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(PASTA, "saida")
os.makedirs(SAIDA, exist_ok=True)

linhas = []
def log(msg=""):
    print(msg)
    linhas.append(str(msg))

def cenario(titulo, funcao):
    log("\n" + "=" * 78)
    log(titulo)
    log("=" * 78)
    try:
        resultado = funcao()
        if isinstance(resultado, tuple):
            df, sql, params = resultado
            log("SQL GERADO:")
            log(sql)
            log(f"PARAMETROS: {params}")
        else:
            df = resultado
        log(f"LINHAS RETORNADAS: {len(df):,}")
        log(df.head(10).to_string(index=False))
        if len(df):
            log(f"SOMA SALES_VALUE: {df['SALES_VALUE'].sum():,.2f}")
        return df
    except Exception as e:
        log(f"EXCECAO ESPERADA -> {type(e).__name__}: {e}")
        return None

try:
    # 1) uso exatamente como o enunciado pede
    cenario(
        "1) USO DO ENUNCIADO: retrieve_data(18, 1, ['2019-01-01', '2019-01-31'])",
        lambda: retrieve_data(18, 1, ["2019-01-01", "2019-01-31"], return_query=True),
    )

    # 2) um dia unico
    cenario(
        "2) DIA UNICO: date=['2019-12-25'] na loja 1",
        lambda: retrieve_data(store_code=1, date=["2019-12-25"], return_query=True),
    )

    # 3) varias lojas e varios produtos de uma vez
    cenario(
        "3) MULTIPLOS VALORES: produtos [18, 19] em lojas [1, 2, 3] no 1o tri de 2019",
        lambda: retrieve_data([18, 19], [1, 2, 3], ["2019-01-01", "2019-03-31"], return_query=True),
    )

    # 4) so o filtro de produto, sem loja nem data
    cenario(
        "4) FILTRO PARCIAL: so o produto 18, sem loja e sem data",
        lambda: retrieve_data(product_code=18, limit=5000, return_query=True),
    )

    # 5) sem filtro nenhum: a trava de seguranca precisa agir
    cenario(
        "5) SEM FILTRO: a trava de limite precisa segurar as 2,1 mi de linhas",
        lambda: retrieve_data(limit=1000),
    )

    # 6) datas invertidas: a funcao reordena e avisa, em vez de devolver vazio
    cenario(
        "6) DATAS INVERTIDAS: ['2019-01-31', '2019-01-01'] deve reordenar sozinho",
        lambda: retrieve_data(18, 1, ["2019-01-31", "2019-01-01"], return_query=True),
    )

    # 7) data em formato errado: precisa estourar mensagem clara
    cenario(
        "7) DATA INVALIDA: '31/01/2019' precisa dar erro explicado",
        lambda: retrieve_data(18, 1, ["31/01/2019"]),
    )

    # 8) loja em texto: precisa dar erro claro, nao silencio
    cenario(
        "8) LOJA INVALIDA: store_code='loja um' precisa dar erro explicado",
        lambda: retrieve_data(18, "loja um"),
    )

    # 9) tentativa de SQL injection: os parametros vinculados neutralizam
    cenario(
        "9) SEGURANCA: tentativa de injection em product_code",
        lambda: retrieve_data("18; DROP TABLE data_product_sales"),
    )

    # 10) prova de consistencia: a funcao tem que bater com o SQL puro
    log("\n" + "=" * 78)
    log("10) PROVA DE CONSISTENCIA: funcao x SQL escrito na mao")
    log("=" * 78)
    from sqlalchemy import text
    from looqbox_data import get_engine
    via_funcao = retrieve_data(18, 1, ["2019-01-01", "2019-01-31"], limit=None)
    via_sql = pd.read_sql(text("""
        SELECT STORE_CODE, PRODUCT_CODE, DATE, SALES_VALUE, SALES_QTY
        FROM data_product_sales
        WHERE PRODUCT_CODE = 18 AND STORE_CODE = '1'
          AND DATE BETWEEN '2019-01-01' AND '2019-01-31'
    """), get_engine())
    log(f"funcao: {len(via_funcao)} linhas | soma {via_funcao['SALES_VALUE'].sum():,.2f}")
    log(f"sql puro: {len(via_sql)} linhas | soma {via_sql['SALES_VALUE'].sum():,.2f}")
    bate = len(via_funcao) == len(via_sql) and abs(
        float(via_funcao["SALES_VALUE"].sum()) - float(via_sql["SALES_VALUE"].sum())
    ) < 0.01
    log(">> RESULTADO: " + ("IGUAL, funcao validada" if bate else "DIFERENTE, investigar"))

    via_funcao.to_csv(os.path.join(SAIDA, "03_case1_exemplo.csv"), index=False, encoding="utf-8-sig")
    log("\n[ok] CASE 1 CONCLUIDO")

except Exception:
    log("\n[XX] ERRO GERAL:")
    log(traceback.format_exc())

with open(os.path.join(SAIDA, "03_case1.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(linhas))

print("\n>>> Saida em: " + SAIDA)
