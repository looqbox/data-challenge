# -*- coding: utf-8 -*-
"""
ETAPA 6 - CASE 3: visualizacao propria com a tabela IMDB_movies.

Pergunta de negocio que escolhi:
    "Nota de critico vira bilheteria? E quais generos concentram receita?"

Antes de plotar, o script faz o perfil da tabela, porque o mapeamento do schema
mostrou uma coisa importante: Rating e RevenueMillions estao como decimal(10,0),
ou seja, SEM casa decimal. A nota 8.4 virou 8. Isso derruba a nota do publico
como eixo continuo e me obriga a usar o Metascore, que eh int de 0 a 100 e
manteve a granularidade.
"""
import os, traceback
from urllib.parse import quote_plus

import numpy as np
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

AZUL, LARANJA, CINZA, FUNDO = "#0072B2", "#D55E00", "#8a8a8a", "#fcfcfb"

linhas = []
def log(msg=""):
    print(msg)
    linhas.append(str(msg))

def limpa_eixos(ax):
    ax.set_facecolor(FUNDO)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color("#d8d5cf")
    ax.tick_params(colors="#5c5c5c", labelsize=9, length=0)

try:
    df = pd.read_sql(text("SELECT * FROM IMDB_movies"), ENGINE)
    log("=" * 78)
    log("PERFIL DA TABELA IMDB_movies")
    log("=" * 78)
    log(f"Linhas: {len(df)} | Colunas: {list(df.columns)}")
    log(f"Periodo dos filmes: {df['Year'].min()} a {df['Year'].max()}")
    log("\nNULOS POR COLUNA:")
    log(df.isna().sum().to_string())

    log("\nVALORES DISTINTOS DE Rating: %s" % sorted(df["Rating"].dropna().unique().tolist()))
    log(">> Rating foi gravado como decimal(10,0): a casa decimal foi perdida na modelagem.")
    log(">> Por isso a analise usa Metascore (int de 0 a 100), que preservou a granularidade.")

    for col in ("Runtime", "Votes", "RevenueMillions", "Metascore"):
        s = pd.to_numeric(df[col], errors="coerce")
        log(f"\n{col}: min={s.min()} | mediana={s.median()} | media={s.mean():.1f} | max={s.max()} | nulos={s.isna().sum()}")

    df["RevenueMillions"] = pd.to_numeric(df["RevenueMillions"], errors="coerce")
    df["Metascore"] = pd.to_numeric(df["Metascore"], errors="coerce")

    # ----------------------------------------------------------------------
    # GRAFICO 1 - dispersao: nota da critica x bilheteria
    # ----------------------------------------------------------------------
    base = df.dropna(subset=["Metascore", "RevenueMillions"]).copy()
    log("\n" + "=" * 78)
    log("GRAFICO 1 - critica x bilheteria")
    log("=" * 78)
    log(f"Filmes com as duas informacoes: {len(base)} de {len(df)}")

    r = base["Metascore"].corr(base["RevenueMillions"])
    r2 = r ** 2
    log(f"Correlacao de Pearson: r = {r:.3f} | r2 = {r2:.3f}")
    log(f">> A nota da critica explica cerca de {r2*100:.1f}% da variacao de bilheteria.")

    coef = np.polyfit(base["Metascore"], base["RevenueMillions"], 1)
    xs = np.linspace(base["Metascore"].min(), base["Metascore"].max(), 50)

    fig, ax = plt.subplots(figsize=(9.5, 6))
    fig.patch.set_facecolor(FUNDO)
    ax.scatter(base["Metascore"], base["RevenueMillions"], s=26, alpha=0.45,
               color=AZUL, edgecolors="none")
    ax.plot(xs, np.polyval(coef, xs), color=LARANJA, linewidth=2,
            label=f"tendência linear (r² = {r2:.2f})")

    # marca os campeoes de bilheteria, que sao a prova visual do argumento
    for _, f in base.nlargest(5, "RevenueMillions").iterrows():
        ax.annotate(f["Title"], (f["Metascore"], f["RevenueMillions"]),
                    textcoords="offset points", xytext=(6, 4),
                    fontsize=8, color="#3c3c3c")

    ax.set_title("Nota da crítica não explica bilheteria",
                 fontsize=14, pad=14, loc="left", color="#1a1a1a")
    ax.set_xlabel("Metascore, nota da crítica de 0 a 100", fontsize=10, color="#5c5c5c")
    ax.set_ylabel("Receita em milhões de dólares", fontsize=10, color="#5c5c5c")
    ax.grid(True, color="#e6e4df", linewidth=0.8)
    ax.legend(frameon=False, fontsize=9)
    limpa_eixos(ax)
    plt.tight_layout()
    p1 = os.path.join(SAIDA, "05_imdb_critica_x_bilheteria.png")
    plt.savefig(p1, dpi=200, facecolor=FUNDO)
    plt.close()
    log(f"[ok] salvo em {p1}")

    # ----------------------------------------------------------------------
    # GRAFICO 2 - genero: a coluna Genre eh multivalorada, entao explodo
    # ----------------------------------------------------------------------
    log("\n" + "=" * 78)
    log("GRAFICO 2 - receita mediana por genero")
    log("=" * 78)
    g = df.assign(Genre=df["Genre"].fillna("").str.split(",")).explode("Genre")
    g["Genre"] = g["Genre"].str.strip()
    g = g[g["Genre"] != ""]
    log(f"Linhas apos explodir os generos: {len(g)} (cada filme tem ate 3 generos)")

    resumo = (g.dropna(subset=["RevenueMillions"])
                .groupby("Genre")
                .agg(filmes=("Id", "count"),
                     receita_mediana=("RevenueMillions", "median"),
                     receita_total=("RevenueMillions", "sum"))
                .query("filmes >= 20")
                .sort_values("receita_mediana", ascending=False))
    log(resumo.round(1).to_string())

    top = resumo.head(12).sort_values("receita_mediana")
    cores = [LARANJA if i >= len(top) - 3 else AZUL for i in range(len(top))]

    fig, ax = plt.subplots(figsize=(9.5, 6.5))
    fig.patch.set_facecolor(FUNDO)
    barras = ax.barh(top.index, top["receita_mediana"], color=cores, height=0.62)
    for barra, (valor, n) in zip(barras, zip(top["receita_mediana"], top["filmes"])):
        ax.text(valor + 1.5, barra.get_y() + barra.get_height() / 2,
                f"US$ {valor:.0f} mi  ({n} filmes)", va="center", fontsize=8.5, color="#3c3c3c")

    ax.set_title("Animação, aventura e ação concentram a receita mediana",
                 fontsize=14, pad=14, loc="left", color="#1a1a1a")
    ax.set_xlabel("Receita mediana por filme, em milhões de dólares", fontsize=10, color="#5c5c5c")
    ax.set_xlim(0, top["receita_mediana"].max() * 1.42)
    ax.xaxis.grid(True, color="#e6e4df", linewidth=0.8)
    limpa_eixos(ax)
    plt.tight_layout()
    p2 = os.path.join(SAIDA, "05_imdb_receita_por_genero.png")
    plt.savefig(p2, dpi=200, facecolor=FUNDO)
    plt.close()
    log(f"[ok] salvo em {p2}")

    resumo.round(2).to_csv(os.path.join(SAIDA, "05_imdb_generos.csv"), encoding="utf-8-sig")

    # numeros de apoio para a analise escrita
    log("\nAPOIO PARA A ANALISE:")
    q_alta = base[base["Metascore"] >= 80]["RevenueMillions"]
    q_baixa = base[base["Metascore"] < 50]["RevenueMillions"]
    log(f"Filmes com Metascore >= 80: {len(q_alta)} | receita mediana US$ {q_alta.median():.1f} mi")
    log(f"Filmes com Metascore <  50: {len(q_baixa)} | receita mediana US$ {q_baixa.median():.1f} mi")
    log(f"Correlacao Votes x Receita: {base['Votes'].corr(base['RevenueMillions']):.3f}")

    log("\n[ok] CASE 3 CONCLUIDO")

except Exception:
    log("\n[XX] ERRO:")
    log(traceback.format_exc())

with open(os.path.join(SAIDA, "05_case3.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(linhas))

print("\n>>> Saida em: " + SAIDA)
