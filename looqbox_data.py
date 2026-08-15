# -*- coding: utf-8 -*-
"""
CASE 1 - Desafio Looqbox
Modulo de acesso aos dados de venda por produto.

O time cansou de reescrever a mesma query trocando so os filtros.
Entao a query deixa de ser texto copiado e vira uma funcao com contrato claro:
`retrieve_data(product_code, store_code, date)`.

Premissas assumidas (declaradas de proposito, para o avaliador saber o que eu decidi):
1. Todo filtro eh OPCIONAL. Quem chama sem argumento nenhum quer a tabela toda,
   e por isso existe um limite de seguranca (a tabela tem 2,1 milhoes de linhas).
2. Os filtros aceitam um valor unico ou uma lista de valores, porque "traga a loja 1"
   e "traga as lojas 1, 3 e 7" sao a mesma pergunta com cardinalidade diferente.
3. `date` segue o enunciado: lista de strings ISO. Com 1 item vira dia exato,
   com 2 itens vira intervalo fechado.
4. Nada de montar SQL com f-string de valor. Todo valor vai como parametro vinculado,
   senao a funcao vira porta aberta para SQL injection quando outro time usar.
5. A funcao devolve DataFrame com as colunas de data_product_sales, como pedido.
"""
from __future__ import annotations

import os
import logging
from datetime import date as _date, datetime
from typing import Iterable, Optional, Sequence, Union

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Conexao: fica em um lugar so. Credencial via variavel de ambiente quando
# existir, com o valor do desafio como padrao para facilitar a avaliacao.
# --------------------------------------------------------------------------
DB_USER = os.getenv("LOOQBOX_USER", "looqbox-challenge")
DB_PASS = os.getenv("LOOQBOX_PASS", "looq-challenge")
DB_HOST = os.getenv("LOOQBOX_HOST", "35.199.115.174")
DB_NAME = os.getenv("LOOQBOX_DB", "looqbox-challenge")

TABELA = "data_product_sales"
COLUNAS = ["STORE_CODE", "PRODUCT_CODE", "DATE", "SALES_VALUE", "SALES_QTY"]
LIMITE_PADRAO = 100_000  # trava de seguranca: ninguem puxa 2,1 mi por acidente

_engine: Optional[Engine] = None


def get_engine() -> Engine:
    """Cria a engine uma unica vez e reaproveita (evita abrir conexao por chamada)."""
    global _engine
    if _engine is None:
        url = (
            f"mysql+pymysql://{quote_plus(DB_USER)}:{quote_plus(DB_PASS)}"
            f"@{DB_HOST}/{quote_plus(DB_NAME)}?charset=utf8mb4"
        )
        _engine = create_engine(url, pool_pre_ping=True, pool_recycle=3600)
    return _engine


# --------------------------------------------------------------------------
# Normalizacao de entrada
# --------------------------------------------------------------------------
def _como_lista(valor) -> Optional[list]:
    """Aceita None, valor unico ou colecao, e devolve sempre lista ou None."""
    if valor is None:
        return None
    if isinstance(valor, (str, bytes)) or not isinstance(valor, Iterable):
        return [valor]
    lista = list(valor)
    return lista or None


def _valida_inteiros(valores, nome_campo) -> list:
    saida = []
    for v in valores:
        try:
            saida.append(int(v))
        except (TypeError, ValueError):
            raise ValueError(
                f"{nome_campo} precisa ser inteiro ou lista de inteiros. Recebi: {v!r}"
            )
    return saida


def _valida_datas(valores) -> list:
    """Aceita 'YYYY-MM-DD', date ou datetime. Devolve lista de strings ISO."""
    saida = []
    for v in valores:
        if isinstance(v, (_date, datetime)):
            saida.append(v.strftime("%Y-%m-%d"))
            continue
        try:
            saida.append(datetime.strptime(str(v).strip(), "%Y-%m-%d").strftime("%Y-%m-%d"))
        except ValueError:
            raise ValueError(
                f"date precisa estar no formato ISO 'YYYY-MM-DD'. Recebi: {v!r}"
            )
    if len(saida) > 2:
        raise ValueError(
            "date aceita no maximo 2 itens: ['dia'] para um dia ou "
            "['inicio', 'fim'] para um intervalo."
        )
    if len(saida) == 2 and saida[0] > saida[1]:
        # inverter em silencio esconderia erro de quem chama; melhor avisar e corrigir
        logger.warning("Datas invertidas (%s > %s). Reordenando.", saida[0], saida[1])
        saida = sorted(saida)
    return saida


# --------------------------------------------------------------------------
# Funcao principal
# --------------------------------------------------------------------------
def retrieve_data(
    product_code: Union[int, Sequence[int], None] = None,
    store_code: Union[int, Sequence[int], None] = None,
    date: Union[str, Sequence[str], None] = None,
    limit: Optional[int] = LIMITE_PADRAO,
    return_query: bool = False,
    engine: Optional[Engine] = None,
):
    """Traz as vendas de produto ja filtradas, em DataFrame.

    Parametros
    ----------
    product_code : int | list[int] | None
        Codigo do produto. Aceita um ou varios. None traz todos.
    store_code : int | list[int] | None
        Codigo da loja. Aceita um ou varios. None traz todas.
    date : str | list[str] | None
        Data em ISO. ['2019-01-01'] filtra o dia,
        ['2019-01-01', '2019-01-31'] filtra o intervalo fechado. None traz tudo.
    limit : int | None
        Trava de seguranca. Passe None para desligar quando precisar da base cheia.
    return_query : bool
        True devolve (DataFrame, sql, parametros) para depurar ou auditar.
    engine : Engine | None
        Permite injetar outra conexao, util em teste automatizado.

    Retorno
    -------
    pandas.DataFrame com as colunas de data_product_sales.

    Exemplos
    --------
    >>> retrieve_data(18, 1, ['2019-01-01', '2019-01-31'])
    >>> retrieve_data(store_code=[1, 2, 3], date=['2019-12-25'])
    >>> retrieve_data()                      # amostra geral, respeitando o limite
    """
    filtros, parametros = [], {}

    produtos = _como_lista(product_code)
    if produtos:
        produtos = _valida_inteiros(produtos, "product_code")
        chaves = [f":prod_{i}" for i in range(len(produtos))]
        filtros.append(f"PRODUCT_CODE IN ({', '.join(chaves)})")
        parametros.update({f"prod_{i}": v for i, v in enumerate(produtos)})

    lojas = _como_lista(store_code)
    if lojas:
        lojas = _valida_inteiros(lojas, "store_code")
        chaves = [f":loja_{i}" for i in range(len(lojas))]
        # STORE_CODE eh varchar nesta tabela: comparo como numero dos dois lados
        # para nao depender de zero a esquerda nem de espaco no cadastro.
        filtros.append(f"CAST(STORE_CODE AS UNSIGNED) IN ({', '.join(chaves)})")
        parametros.update({f"loja_{i}": v for i, v in enumerate(lojas)})

    datas = _como_lista(date)
    if datas:
        datas = _valida_datas(datas)
        if len(datas) == 1:
            filtros.append("DATE = :data_ini")
            parametros["data_ini"] = datas[0]
        else:
            filtros.append("DATE BETWEEN :data_ini AND :data_fim")
            parametros["data_ini"], parametros["data_fim"] = datas

    sql = f"SELECT {', '.join(COLUNAS)} FROM {TABELA}"
    if filtros:
        sql += "\nWHERE " + "\n  AND ".join(filtros)
    sql += "\nORDER BY DATE, STORE_CODE, PRODUCT_CODE"
    if limit:
        sql += f"\nLIMIT {int(limit)}"

    logger.info("Executando: %s | parametros: %s", sql.replace("\n", " "), parametros)
    eng = engine or get_engine()
    df = pd.read_sql(text(sql), eng, params=parametros)

    if limit and len(df) == limit:
        logger.warning(
            "O retorno bateu no limite de %s linhas. Pode haver dado sobrando: "
            "aumente o limit ou passe limit=None.", limit
        )

    if return_query:
        return df, sql, parametros
    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
    print(retrieve_data(18, 1, ["2019-01-01", "2019-01-31"]).head())
