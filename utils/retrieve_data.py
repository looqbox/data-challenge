import os
import numpy as np
import pandas as pd

def retrieve_data(df, product_code, store_code, date):
    """
    Filtra o DataFrame de vendas por produto, loja e intervalo de datas,
    exporta o resultado em .csv e retorna o DataFrame filtrado.
    
    Responde às perguntas:
    'Como otimizar as consultas independente dos filtros ?'

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame bruto gerado pela consulta ao banco MySQL (df_raw_sales).
    
    product_code : int, list ou None
        Código do produto. Aceita valor único, lista de códigos ou None
        (retorna DataFrame vazio).
        Exemplo 1: [18, 19, 20] -> Produtos especificos
        Exemplo 2: range(18, 21) -> Intervalo de Produtos
    
    store_code : int, list ou None
        Código da loja. Aceita valor único, lista de códigos ou None
        (retorna DataFrame vazio).
        Exemplo 1: [18, 19, 20] -> Lojas especificos
        Exemplo 2: range(18, 21) -> Intervalo de Lojas
    
    date : list of str
        Intervalo de datas no formato ISO. Sempre dois elementos:
        Exemplo 1: ['2019-01-01', '2019-01-31'] → range de datas.
        Exemplo 2: ['2019-01-15', '2019-01-15'] → data única para fitrar apenas um dia.
    
    Retorna
    -------
    df_final : pd.DataFrame
        DataFrame filtrado com as colunas na ordem:
        STORE_CODE, PRODUCT_CODE, DATE, SALES_VALUE, SALES_QTY.
    """
    
    # 1. Validação de entrada
    
    if product_code is None or store_code is None or date is None:
        return pd.DataFrame(columns=['STORE_CODE', 'PRODUCT_CODE', 'DATE', 'SALES_VALUE', 'SALES_QTY'])
    
    # 1.1 Cria uma cópia do Dataframe Original para Manipulação
    df1 = df.copy()
    
    # 2. Ajusta todos os tipos de dados do dataset (transformação do )
    df1['STORE_CODE'] = df1["STORE_CODE"].astype(int)
    df1['DATE'] = pd.to_datetime(df1['DATE'])
    
    # 3. Lista as variaveis de filtro para o dataset
    flt_product_code = np.atleast_1d(product_code)
    flt_store_code = np.atleast_1d(store_code)
    flt_date_start = pd.to_datetime(date[0])
    flt_date_end = pd.to_datetime(date[1])
    
    # 4. Cria o filtro para passar no dataset
    filtro = (
        df1['STORE_CODE'].isin(flt_store_code) &
        df1['PRODUCT_CODE'].isin(flt_product_code) &
        df1['DATE'].between(flt_date_start, flt_date_end)
    )
    df_filtro = df1.loc[filtro]
    
    # 5. Organiza as colunas do dataset para exportação final (em caso de personalização de exportação)
    cols_ordem = ['STORE_CODE', 'PRODUCT_CODE', 'DATE', 'SALES_VALUE', 'SALES_QTY']
    df_final = df_filtro[cols_ordem].reset_index(drop=True)
    
    # 6. Exporta o df_final em .csv para utilização em outros SAAS
    output_dir  = os.path.abspath(os.path.join(os.getcwd(), "..", "02_retrieve_data", "data"))
    filename    = f"{product_code}_{store_code}_{date[0]}_{date[1]}.csv"
    output_path = os.path.join(output_dir, filename)
    
    os.makedirs(output_dir, exist_ok=True)
    df_final.to_csv(output_path, index=False, sep=";", encoding="utf-8-sig")
    
    return df_final