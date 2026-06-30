'''
Case 2 - Join e agregacao de vendas por loja em pandas

O que este script faz:
1. Conecta no banco (mesmo .env dos outros cases) e executa DUAS queries,
   exatamente como fornecidas, SEM nenhuma alteracao no SQL:
   - data_store_cad   : cadastro das lojas (nome, negocio, vigencia).
   - data_store_sales : vendas do ano de 2019 inteiro.
2. Faz TODO o tratamento em pandas (nada e calculado no SQL):
   - converte tipos (valores numericos e datas);
   - inner join entre as duas tabelas por STORE_CODE;
   - filtra as datas no intervalo ['2019-10-01', '2019-12-31'];
   - agrupa por STORE_CODE e soma SALES_VALUE e SALES_QTY;
   - calcula o TM (SUM SALES_VALUE / SUM SALES_QTY).
3. Apresenta o resultado no terminal com as colunas:
   STORE_NAME, BUSINESS_NAME, TM.
   (SUM SALES_VALUE e SUM SALES_QTY sao calculados internamente para o TM.)

'''

import os
from decimal import ROUND_HALF_UP, Decimal

import pandas as pd
import pymysql
from dotenv import load_dotenv

load_dotenv()


def arredondar_meio_para_cima(valor, casas=2):
    if pd.isna(valor):
        return valor
    quantum = Decimal('1').scaleb(-casas) 
    return float(Decimal(str(valor)).quantize(quantum, rounding=ROUND_HALF_UP))

DATA_INICIO = '2019-10-01'
DATA_FIM = '2019-12-31'

# Queries fornecidas - NAO devem ser alteradas.
QUERY_CAD = """
SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
FROM data_store_cad
"""

QUERY_SALES = """
SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
"""


def get_connection():
    """Abre uma nova conexao com o banco usando as variaveis do .env."""
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT', 3306)),
        cursorclass=pymysql.cursors.DictCursor,
    )


def carregar_dados():
    """Executa as duas queries e devolve dois DataFrames (cad, sales)."""
    conexao = get_connection()
    try:
        with conexao.cursor() as cursor:
            cursor.execute(QUERY_CAD)
            cad = pd.DataFrame(cursor.fetchall())

            cursor.execute(QUERY_SALES)
            sales = pd.DataFrame(cursor.fetchall())
    finally:
        conexao.close()
    return cad, sales


def tratar_dados(cad, sales):
    """Converte tipos, faz inner join por STORE_CODE e filtra as datas."""
    sales = sales.copy()

    # Valores podem vir como Decimal/None -> converte para numerico.
    sales['SALES_VALUE'] = pd.to_numeric(sales['SALES_VALUE'], errors='coerce')
    sales['SALES_QTY'] = pd.to_numeric(sales['SALES_QTY'], errors='coerce')
    sales['DATE'] = pd.to_datetime(sales['DATE'], errors='coerce')

    # Inner join entre vendas e cadastro pelo STORE_CODE.
    df = pd.merge(sales, cad, on='STORE_CODE', how='inner')

    # Filtro de datas feito em pandas (inclusivo nas duas pontas).
    inicio = pd.Timestamp(DATA_INICIO)
    fim = pd.Timestamp(DATA_FIM)
    df = df[(df['DATE'] >= inicio) & (df['DATE'] <= fim)]

    return df


def agregar(df):
    """Agrupa por STORE_CODE, soma os valores e calcula o TM."""
    agrupado = df.groupby('STORE_CODE').agg(
        STORE_NAME=('STORE_NAME', 'first'),
        BUSINESS_NAME=('BUSINESS_NAME', 'first'),
        sum_sales_value=('SALES_VALUE', 'sum'),
        sum_sales_qty=('SALES_QTY', 'sum'),
    ).reset_index()

    # TM = ticket medio. Evita divisao por zero (vira NaN quando QTY == 0).
    agrupado['TM'] = agrupado['sum_sales_value'].div(
        agrupado['sum_sales_qty'].where(agrupado['sum_sales_qty'] != 0)
    )

    # Seleciona e renomeia as colunas na ordem pedida.
    resultado = agrupado[[
        'STORE_NAME',
        'BUSINESS_NAME',
        #'sum_sales_value',
        #'sum_sales_qty',
        'TM',
    ]].rename(columns={
        #'sum_sales_value': 'SUM SALES_VALUE',
        #'sum_sales_qty': 'SUM SALES_QTY',
    })

    # Arredonda (metade para cima) com 2 casas decimais.
    for coluna in ['TM']:  # 'SUM SALES_VALUE', 'SUM SALES_QTY'
        resultado[coluna] = resultado[coluna].apply(arredondar_meio_para_cima)

    # Ordena por ordem alfabetica de STORE_NAME.
    resultado = resultado.sort_values('STORE_NAME').reset_index(drop=True)

    return resultado


def main():
    print('Carregando dados das tabelas data_store_cad e data_store_sales...')
    cad, sales = carregar_dados()
    print(f'  cad: {len(cad)} linhas | sales: {len(sales)} linhas')

    df = tratar_dados(cad, sales)
    print(f'  Apos join e filtro de datas '
          f'({DATA_INICIO} a {DATA_FIM}): {len(df)} linhas')

    resultado = agregar(df)

    print('\nResultado por loja:\n')
    print(resultado.to_string(index=False))


if __name__ == '__main__':
    main()
