import pandas as pd
from database import get_engine

engine = get_engine()

def get_ticket_medio_by_store():
    query_store = """
    SELECT
        STORE_CODE,
        STORE_NAME,
        START_DATE,
        END_DATE,
        BUSINESS_NAME,
        BUSINESS_CODE
    FROM data_store_cad
    """
    query_sales = """
    SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
    FROM data_store_sales
    WHERE
        DATE BETWEEN '2019-01-01' AND '2019-12-31'
    """
    
    df_store = pd.read_sql_query(query_store, engine)
    df_sales = pd.read_sql_query(query_sales, engine)
    
    #Converte a coluna DATE para datetime
    df_sales['DATE'] = pd.to_datetime(df_sales['DATE'])

    df_sales = df_sales[
        (df_sales['DATE'] >= '2019-10-01') & 
        (df_sales['DATE'] <= '2019-12-31')
    ]

    df = df_sales.merge(df_store, on='STORE_CODE', how='left')

    df_grouped = df.groupby(['STORE_NAME', 'BUSINESS_NAME']).agg(
        TOTAL_VAL=('SALES_VALUE', 'sum'),
        TOTAL_QTY=('SALES_QTY', 'sum')
    ).reset_index()

    df_grouped['TM'] = df_grouped['TOTAL_VAL'] / df_grouped['TOTAL_QTY']
    
    df_grouped['TM'] = df_grouped['TM'].round(2)

    df_final = df_grouped.rename(columns={
        'STORE_NAME': 'Loja',
        'BUSINESS_NAME': 'Categoria'
    })

    return df_final[['Loja', 'Categoria', 'TM']].sort_values(by='TM', ascending=False)