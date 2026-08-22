# -*- coding: utf-8 -*-
"""
ETAPA 1b - Desafio Looqbox
O erro 1044 mostrou que o login funciona, mas o nome do schema estava errado.
O e-mail fala em "looqbox-challenge" (com hifen) e o README em "looqbox_challenge".
Este script conecta SEM escolher schema, descobre o nome verdadeiro e mapeia tudo.
"""
import os, json, traceback
import pymysql
import pandas as pd

PASTA = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(PASTA, "saida")
os.makedirs(SAIDA, exist_ok=True)

linhas = []
def log(msg=""):
    print(msg)
    linhas.append(str(msg))

CONF = dict(
    host="35.199.115.174",
    user="looqbox-challenge",
    password="looq-challenge",
    connect_timeout=20,
    charset="utf8mb4",
)

resumo = {"tabelas": {}}
SISTEMA = {"information_schema", "performance_schema", "mysql", "sys"}

try:
    log(">>> Conectando SEM schema definido ...")
    con = pymysql.connect(**CONF)
    cur = con.cursor()
    log("[ok] conectado")

    cur.execute("SHOW DATABASES")
    todos = [r[0] for r in cur.fetchall()]
    log(f"\nSCHEMAS VISIVEIS: {todos}")
    resumo["schemas"] = todos

    alvos = [d for d in todos if d not in SISTEMA]
    log(f"SCHEMAS DE TRABALHO: {alvos}")

    for db in alvos:
        log("\n" + "=" * 70)
        log(f"SCHEMA: {db}")
        log("=" * 70)
        cur.execute(f"USE `{db}`")
        cur.execute("SHOW TABLES")
        tabelas = [r[0] for r in cur.fetchall()]
        log(f"TABELAS ({len(tabelas)}): {tabelas}")

        for t in tabelas:
            log("\n" + "-" * 70)
            log(f"TABELA: {db}.{t}")
            log("-" * 70)
            cur.execute(f"DESCRIBE `{db}`.`{t}`")
            cols = cur.fetchall()
            colnames = [c[0] for c in cols]
            for c in cols:
                log(f"   {c[0]:<22} {c[1]:<18} null={c[2]:<4} key={c[3]}")

            cur.execute(f"SELECT COUNT(*) FROM `{db}`.`{t}`")
            qtd = cur.fetchone()[0]
            log(f"   >> LINHAS: {qtd:,}")

            amostra = pd.read_sql(f"SELECT * FROM `{db}`.`{t}` LIMIT 5", con)
            log("   >> AMOSTRA:")
            log(amostra.to_string(index=False))

            info = {
                "schema": db,
                "colunas": [{"nome": c[0], "tipo": c[1]} for c in cols],
                "linhas": int(qtd),
                "amostra": json.loads(amostra.to_json(orient="records", date_format="iso")),
            }

            for cand in ("DATE", "date", "Date"):
                if cand in colnames:
                    cur.execute(f"SELECT MIN(`{cand}`), MAX(`{cand}`) FROM `{db}`.`{t}`")
                    dmin, dmax = cur.fetchone()
                    log(f"   >> PERIODO: {dmin} ate {dmax}")
                    info["periodo"] = [str(dmin), str(dmax)]
                    break

            resumo["tabelas"][f"{db}.{t}"] = info

    con.close()
    log("\n[ok] MAPEAMENTO CONCLUIDO")

except Exception:
    log("\n[XX] ERRO:")
    log(traceback.format_exc())

with open(os.path.join(SAIDA, "01_schema.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(linhas))
with open(os.path.join(SAIDA, "01_schema.json"), "w", encoding="utf-8") as f:
    json.dump(resumo, f, ensure_ascii=False, indent=2, default=str)

print("\n>>> Saida em: " + SAIDA)
