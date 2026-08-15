# -*- coding: utf-8 -*-
"""
ETAPA 5 - CASE 2: TM por loja no 4o trimestre de 2019.

Regras do cliente que eu segui a risca:
  - as duas queries entram EXATAMENTE como ele mandou, sem uma virgula alterada;
  - o recorte ['2019-10-01', '2019-12-31'] eh aplicado DEPOIS, no Python.

Sobre o TM: o enunciado nao define a formula. Testei as duas leituras possiveis e
mantive a que reproduz a tabela esperada do desafio:
  A) TM = SOMA(SALES_VALUE) / SOMA(SALES_QTY)   -> ticket medio do periodo
  B) TM = MEDIA(SALES_VALUE / SALES_QTY)        -> media das medias diarias
"""
import os, json, traceback
from urllib.parse import quote_plus

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text

PASTA = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(PASTA, "saida")
os.makedirs(SAIDA, exist_ok=True)

ENGINE = create_engine(
    "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(
        quote_plus("looqbox-challenge"), quote_plus("looq-challenge"),
        "35.199.115.174", quote_plus("looqbox-challenge")
    ), pool_pre_ping=True,
)

linhas = []
def log(msg=""):
    print(msg)
    linhas.append(str(msg))

# --------------------------------------------------------------------------
# As duas queries do cliente, INTOCADAS
# --------------------------------------------------------------------------
QUERY_1 = """
SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
FROM data_store_cad
"""

QUERY_2 = """
SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
"""

PERIODO = ["2019-10-01", "2019-12-31"]

# tabela que o desafio mostra como resultado esperado, usada so para conferencia
ESPERADO = {
    "Bahia": ("Atacado", 15.39), "Bangkok": ("Posto", 13.67), "Belem": ("Proximidade", 15.37),
    "Berlin": ("Proximidade", 15.39), "Buenos Aires": ("Atacado", 15.39), "Chicago": ("Varejo", 15.53),
    "Dubai": ("Atacado", 15.39), "Hong Kong": ("Farma", 26.35), "London": ("Farma", 28.99),
    "Madri": ("Farma", 29.03), "Miami": ("Posto", 13.67), "New York": ("Proximidade", 15.39),
    "Paris": ("Proximidade", 15.39), "Rio de Janeiro": ("Farma", 29.59), "Roma": ("Varejo", 15.39),
    "Salvador": ("Atacado", 15.39), "Sao Paulo": ("Varejo", 15.39), "Sidney": ("Posto", 13.67),
    "Tokio": ("Varejo", 15.39), "Vancouver": ("Posto", 13.67),
}

# paleta categorica testada para daltonismo (base Okabe-Ito)
CORES = {
    "Farma": "#0072B2", "Varejo": "#E69F00", "Atacado": "#009E73",
    "Proximidade": "#D55E00", "Posto": "#CC79A7",
}

try:
    log("=" * 78)
    log("PASSO 1 - executar as duas queries do cliente sem alterar nada")
    log("=" * 78)
    lojas = pd.read_sql(text(QUERY_1), ENGINE)
    vendas = pd.read_sql(text(QUERY_2), ENGINE)
    log(f"Query 1 (cadastro de lojas): {len(lojas)} linhas")
    log(f"Query 2 (vendas de 2019 inteiro): {len(vendas):,} linhas")

    log("\n" + "=" * 78)
    log("PASSO 2 - aplicar o recorte pedido no Python: %s a %s" % tuple(PERIODO))
    log("=" * 78)
    vendas["DATE"] = pd.to_datetime(vendas["DATE"])
    ini, fim = pd.to_datetime(PERIODO[0]), pd.to_datetime(PERIODO[1])
    q4 = vendas[(vendas["DATE"] >= ini) & (vendas["DATE"] <= fim)].copy()
    log(f"Linhas depois do filtro: {len(q4):,} (de {len(vendas):,})")
    log(f"Periodo real no dado: {q4['DATE'].min().date()} ate {q4['DATE'].max().date()}")
    log(f"Lojas no periodo: {q4['STORE_CODE'].nunique()}")

    log("\n" + "=" * 78)
    log("PASSO 3 - calcular o TM pelas duas leituras possiveis e escolher a certa")
    log("=" * 78)
    q4["TM_LINHA"] = q4["SALES_VALUE"] / q4["SALES_QTY"]
    agr = q4.groupby("STORE_CODE").agg(
        SALES_VALUE=("SALES_VALUE", "sum"),
        SALES_QTY=("SALES_QTY", "sum"),
        TM_MEDIA_DAS_MEDIAS=("TM_LINHA", "mean"),
    ).reset_index()
    agr["TM_SOMA_SOBRE_SOMA"] = (agr["SALES_VALUE"] / agr["SALES_QTY"]).round(2)
    agr["TM_MEDIA_DAS_MEDIAS"] = agr["TM_MEDIA_DAS_MEDIAS"].round(2)

    # junta com o cadastro para trazer nome e categoria da loja
    base = agr.merge(lojas[["STORE_CODE", "STORE_NAME", "BUSINESS_NAME"]], on="STORE_CODE", how="left")
    base = base.rename(columns={"STORE_NAME": "Loja", "BUSINESS_NAME": "Categoria"})

    conf = base[["Loja", "Categoria", "TM_SOMA_SOBRE_SOMA", "TM_MEDIA_DAS_MEDIAS"]].copy()
    conf["TM_ESPERADO"] = conf["Loja"].map(lambda x: ESPERADO.get(x, (None, None))[1])
    conf["DIF_A"] = (conf["TM_SOMA_SOBRE_SOMA"] - conf["TM_ESPERADO"]).round(2)
    conf["DIF_B"] = (conf["TM_MEDIA_DAS_MEDIAS"] - conf["TM_ESPERADO"]).round(2)
    conf = conf.sort_values("Loja")
    log(conf.to_string(index=False))

    acertos_a = int((conf["DIF_A"].abs() <= 0.01).sum())
    acertos_b = int((conf["DIF_B"].abs() <= 0.01).sum())
    log(f"\nFormula A (soma/soma)      bate em {acertos_a} de {len(conf)} lojas")
    log(f"Formula B (media das medias) bate em {acertos_b} de {len(conf)} lojas")
    escolhida = "TM_SOMA_SOBRE_SOMA" if acertos_a >= acertos_b else "TM_MEDIA_DAS_MEDIAS"
    log(f">> FORMULA ADOTADA: {escolhida}")

    log("\n" + "=" * 78)
    log("PASSO 4 - tabela final no formato pedido pelo cliente")
    log("=" * 78)
    final = base[["Loja", "Categoria", escolhida]].rename(columns={escolhida: "TM"})
    final = final.sort_values("Loja").reset_index(drop=True)
    log(final.to_string(index=False))
    final.to_csv(os.path.join(SAIDA, "04_case2_tm.csv"), index=False, encoding="utf-8-sig")

    log("\n" + "=" * 78)
    log("PASSO 5 - visualizacao")
    log("=" * 78)

    g = final.sort_values("TM", ascending=True)
    cores = [CORES.get(c, "#777777") for c in g["Categoria"]]

    fig, ax = plt.subplots(figsize=(9.5, 7))
    fig.patch.set_facecolor("#fcfcfb")
    ax.set_facecolor("#fcfcfb")
    barras = ax.barh(g["Loja"], g["TM"], color=cores, height=0.62)

    for barra, valor in zip(barras, g["TM"]):
        ax.text(valor + 0.35, barra.get_y() + barra.get_height() / 2,
                f"{valor:.2f}".replace(".", ","), va="center", ha="left",
                fontsize=9, color="#3c3c3c")

    ax.set_title("Ticket médio por loja, 4º trimestre de 2019",
                 fontsize=14, pad=16, loc="left", color="#1a1a1a")
    ax.set_xlabel("TM em R$ por unidade vendida", fontsize=10, color="#5c5c5c")
    ax.set_xlim(0, g["TM"].max() * 1.16)
    ax.tick_params(axis="y", labelsize=10, length=0)
    ax.tick_params(axis="x", labelsize=9, colors="#5c5c5c", length=0)
    ax.xaxis.grid(True, color="#e6e4df", linewidth=0.8)
    ax.set_axisbelow(True)
    for lado in ("top", "right", "bottom", "left"):
        ax.spines[lado].set_visible(False)

    ordem = ["Farma", "Varejo", "Atacado", "Proximidade", "Posto"]
    presentes = [c for c in ordem if c in set(final["Categoria"])]
    handles = [plt.Rectangle((0, 0), 1, 1, color=CORES[c]) for c in presentes]
    ax.legend(handles, presentes, title="Categoria", loc="lower right",
              frameon=False, fontsize=9, title_fontsize=9)

    plt.tight_layout()
    caminho = os.path.join(SAIDA, "04_case2_tm.png")
    plt.savefig(caminho, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    log(f"[ok] grafico salvo em {caminho}")

    # leitura de negocio, para eu escrever a analise no PDF
    log("\nRESUMO POR CATEGORIA:")
    log(final.groupby("Categoria")["TM"].agg(["min", "max", "mean", "count"]).round(2).to_string())

    log("\n[ok] CASE 2 CONCLUIDO")

except Exception:
    log("\n[XX] ERRO:")
    log(traceback.format_exc())

with open(os.path.join(SAIDA, "04_case2.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(linhas))

print("\n>>> Saida em: " + SAIDA)
